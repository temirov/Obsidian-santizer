import logging
from pathlib import Path

import constants
from logger.logger import Logger
from services.file_pair import FilePair
from services.markdown_renaming_service import MarkdownRenamingService
from utils.path_utils import PathUtils
from utils.string_utils import StringUtils
from utils.system_utils import SystemUtils


class PathSanitizer:
    def __init__(self, source_folder: str, glob: str, logger: Logger, path_utils: PathUtils, string_utils: StringUtils,
                 system_utils: SystemUtils):
        self.source_folder = source_folder
        self.glob = glob
        self.logger = logger
        self.path_utils = path_utils
        self.string_utils = string_utils
        self.system_utils = system_utils

    def remove_mac_system_files(self) -> bool:
        def walker_function():
            for file_path in self.path_utils.glob_path_walker(self.source_folder, constants.ALL_FILES):
                if self.path_utils.is_mac_system_file(file_path):
                    self.system_utils.bool_func_wrapper(file_path.unlink)

        return self.system_utils.bool_func_wrapper(walker_function)

    def remove_empty_folders(self) -> bool:
        def walker_function():
            for dir_path in self.path_utils.glob_path_walker(self.source_folder, constants.ALL_FILES):
                if self.path_utils.is_empty_dir(dir_path):
                    self.system_utils.bool_func_wrapper(dir_path.rmdir)

        return self.system_utils.bool_func_wrapper(walker_function)

    def remove_empty_files(self) -> bool:
        def walker_function():
            for file_path in self.path_utils.glob_path_walker(self.source_folder, constants.ALL_FILES):
                if self.path_utils.is_empty_file(file_path):
                    self.system_utils.bool_func_wrapper(file_path.unlink)

        return self.system_utils.bool_func_wrapper(walker_function)

    def move_to_resources_folder(self, resource_folder: Path) -> bool:
        def walker_function():
            for file_path in self.path_utils.glob_path_walker(self.source_folder, constants.ALL_FILES):
                if (file_path.is_file()
                        and not self.path_utils.is_in_folder(file_path, constants.OBSIDIAN_RESOURCE_FOLDER)
                        and not self.path_utils.is_json_file(file_path)
                        and self.path_utils.is_application_file(file_path)):
                    destination = resource_folder.joinpath(file_path.name)
                    if not destination.exists():
                        self.system_utils.bool_func_wrapper(file_path.rename, destination)
                    else:
                        self.logger.log(f"The file {destination} already exists", logging.WARN)
                        if file_path.stat().st_size == destination.stat().st_size:
                            self.logger.log(f"The files are identical, deleting {file_path}", logging.WARN)
                            self.system_utils.bool_func_wrapper(file_path.unlink)

        return self.system_utils.bool_func_wrapper(walker_function)

    def rename_markdown_files_with_no_extension(self) -> bool:
        def walker_function():
            for file_path in self.path_utils.glob_path_walker(self.source_folder, constants.ALL_FILES):
                if not self.path_utils.is_hidden(file_path) and self.path_utils.is_md_candidate(file_path):
                    new_file_name = file_path.with_suffix(constants.MARKDOWN_EXTENSION)
                    file_pair = FilePair(file_path, new_file_name, self.system_utils, self.string_utils)
                    markdown_renaming_service = MarkdownRenamingService(file_pair)

                    self.system_utils.bool_func_wrapper(markdown_renaming_service)

        return self.system_utils.bool_func_wrapper(walker_function)

    def rename_similar_markdown_files(self) -> bool:
        def walker_function():
            for file_path in self.path_utils.glob_path_walker(self.source_folder, self.glob):
                if not self.path_utils.is_hidden(file_path) and self.path_utils.is_markup_file(file_path):
                    file_path_without_suffix = StringUtils.expand_and_remove_suffix(file_path.as_posix(), self.glob)
                    new_file_name = self.path_utils.as_path(file_path_without_suffix)
                    file_pair = FilePair(file_path, new_file_name, self.system_utils, self.string_utils)
                    md_renaming_service = MarkdownRenamingService(file_pair)

                    self.system_utils.bool_func_wrapper(md_renaming_service)

        return self.system_utils.bool_func_wrapper(walker_function)

    def move_folders(self, glob: str) -> bool:
        """

        :param glob: A glob string
        :return true if success, false if there were any errors:
        """

        def walker_function():
            for dir_path in self.path_utils.glob_path_walker(self.source_folder, glob):
                if dir_path.is_dir():
                    destination: str = StringUtils.expand_and_remove_suffix(dir_path.as_posix(), glob)
                    if not self.path_utils.as_path(destination).exists():
                        self.system_utils.bool_func_wrapper(dir_path.rename, destination)
                    else:
                        self.logger.log(f"The folder {destination} already exists", logging.ERROR)

        return self.system_utils.bool_func_wrapper(walker_function)

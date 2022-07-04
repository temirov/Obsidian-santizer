from functools import cache
from pathlib import Path

from services.file_cmp import FileCmp
from logger.logger import Logger
from services.file_comparison_service import FileComparisonService
from services.merge_and_delete_service import MergeAndDeleteService
from utils.string_utils import StringUtils
from utils.system_utils import SystemUtils


class FileRenamingService:
    def __init__(self, file_path1: Path, file_path2: Path, string_utils: StringUtils, system_utils: SystemUtils,
                 logger: Logger) -> None:
        self.left_file = file_path1
        self.right_file = file_path2
        self.string_utils = string_utils
        self.system_utils = system_utils
        self.logger = logger

    @cache
    def __file_cmp_result__(self) -> FileCmp:
        file_comparison_service = FileComparisonService(self.left_file, self.right_file, self.string_utils)
        return file_comparison_service()

    def __call__(self, *args, **kwargs) -> None:
        if self.__file_cmp_result__() == FileCmp.IDENTICAL or self.__file_cmp_result__() == FileCmp.LEFT_CONTAINS_RIGHT:
            self.logger.log(f"The {self.left_file} contains {self.right_file}\nDeleting {self.right_file}")
            self.right_file.unlink()
        elif self.__file_cmp_result__() == FileCmp.RIGHT_CONTAINS_LEFT:
            self.logger.log(f"The {self.right_file} contains {self.left_file}\nDeleting {self.left_file}")
            self.left_file.unlink()
        elif self.__file_cmp_result__() == FileCmp.DIFFERENT:
            self.logger.log(f"The files {self.left_file} and {self.right_file} are different. Invoking merge program.")
            merge_and_delete_service = MergeAndDeleteService(self.left_file,
                                                             self.right_file,
                                                             self.system_utils,
                                                             self.string_utils,
                                                             self.logger)
            merge_and_delete_service()

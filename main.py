#!/usr/bin/env python3

import argparse
import logging
from pathlib import Path

import constants
import converters
from logger.logger import Logger
from path_sanitizer import PathSanitizer
from utils.path_utils import PathUtils
from utils.string_utils import StringUtils
from utils.system_utils import SystemUtils


def __parse_args():
    usage = """
        %(prog)s --source <OBSIDIAN_FOLDER> --glob <GLOB> --log <WARN|INFO|DEBUG>
        """
    parser = argparse.ArgumentParser(description='Runs Obsidian.md Sanitizer', usage=usage)
    parser.add_argument('--source',
                        help='folder that contains Obsidian.md notes',
                        type=converters.string_to_path,
                        dest='source_folder',
                        required=True)
    parser.add_argument('--log',
                        help='Set logging level, the default is WARNING',
                        type=converters.string_to_loglevel,
                        default=logging.WARN,
                        dest='log_level')
    parser.add_argument('--glob',
                        help=f'Glob pattern in file names to match',
                        dest='glob',
                        required=True)

    return parser.parse_args()


def __sanitize_system__(path_sanitizer: PathSanitizer, resource_folder: Path, glob: str) -> bool:
    return path_sanitizer.remove_mac_system_files() \
           and path_sanitizer.remove_empty_files() \
           and path_sanitizer.remove_empty_folders() \
           and path_sanitizer.move_folders(f"*{constants.MARKDOWN_EXTENSION}") \
           and path_sanitizer.move_folders(glob) \
           and path_sanitizer.rename_markdown_files_with_no_extension() \
           and path_sanitizer.rename_similar_markdown_files() \
           and path_sanitizer.move_to_resources_folder(resource_folder)


def main() -> None:
    arguments = __parse_args()
    logger = Logger(arguments.log_level)
    path_utils = PathUtils()
    resource_folder = PathUtils.as_path(arguments.source_folder).joinpath(constants.OBSIDIAN_RESOURCE_FOLDER)

    for folder in [arguments.source_folder, resource_folder]:
        path_utils.raise_when_no_folder(folder)

    system_utils = SystemUtils(logger)
    string_utils = StringUtils()

    path_sanitizer = PathSanitizer(
        arguments.source_folder,
        arguments.glob,
        logger,
        path_utils,
        string_utils,
        system_utils
    )

    if __sanitize_system__(path_sanitizer, resource_folder, arguments.glob):
        logger.log("DONE")


if __name__ == '__main__':
    main()

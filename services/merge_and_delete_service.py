import logging
from pathlib import Path

from simple_term_menu import TerminalMenu

from logger.logger import Logger
from utils.string_utils import StringUtils
from utils.system_utils import SystemUtils


class MergeAndDeleteService:
    def __init__(self, left_file: Path, right_file: Path, system_utils: SystemUtils, string_utils: StringUtils,
                 logger: Logger):
        self.left_file = left_file
        self.right_file = right_file
        self.system_utils = system_utils
        self.string_utils = string_utils
        self.logger = logger

    def __call__(self, *args, **kwargs):
        self.system_utils.open_merge_program(self.left_file, self.right_file)
        choices = {0: self.left_file, 1: self.right_file, 2: None}
        options = [f"Delete {choices[0]}", f"Delete {choices[1]}", "Do nothing"]
        terminal_menu = TerminalMenu(options)
        menu_entry_index = terminal_menu.show()
        self.logger.log(f"You have selected {options[menu_entry_index]}!")
        file_to_delete = choices[menu_entry_index]
        if file_to_delete is None:
            self.logger.log(
                f"both {self.left_file} and {self.right_file} still exist!",
                logging.WARNING)
        else:
            file_to_delete.unlink()
            # flip over 1 to 0 and 0 to 1
            remaining_file = choices[1 - menu_entry_index]
            self.logger.log(f"File {remaining_file} remains")
            # if StringUtils.has_glob_suffix(remaining_file.full_path, glob):
            #     self.logger.log(f"Moving file {remaining_file.full_path} to {file_path_without_suffix}")
            #     self.path_utils.move_file(remaining_file.full_path, file_path_without_suffix)

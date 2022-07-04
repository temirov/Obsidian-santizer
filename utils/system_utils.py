import logging
import platform
import subprocess
from pathlib import Path
from typing import Any

import constants
from logger.logger import Logger


class SystemUtils:
    def __init__(self, logger: Logger):
        self.logger = logger

    def bool_func_wrapper(self, function, *args: Any) -> bool:
        try:
            if args is None:
                function()
            else:
                function(*args)
        except OSError as err:
            self.logger.log(str(err), logging.ERROR)
            return False
        else:
            return True

    @classmethod
    def __os(cls) -> str:
        return platform.system()

    @classmethod
    def __is_mac_os(cls) -> bool:
        return cls.__os() == constants.MAC_OS

    def open_merge_program(self, left_filepath: Path, right_filepath: Path, merge_program: str = None) -> bool:
        if self.__is_mac_os():  # macOS
            if merge_program is None:
                merge_program = constants.MAC_MERGE_PROGRAM

            try:
                subprocess.check_call((merge_program, left_filepath, right_filepath))
            except subprocess.CalledProcessError as err:
                self.logger.log(str(err), logging.ERROR)
                return False
            else:
                return True
        else:
            raise RuntimeError(f"Unknown OS: {self.__os()}. The supported OS: Mac")

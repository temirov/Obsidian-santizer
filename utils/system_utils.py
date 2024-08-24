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

    @classmethod
    def __is_linux(cls) -> bool:
        return cls.__os() == constants.Linux_OS

    def open_merge_program(self, left_filepath: Path, right_filepath: Path, merge_program: str = None) -> bool:
        try:
            subprocess.check_call((merge_program, left_filepath, right_filepath))
        except subprocess.CalledProcessError as err:
            self.logger.log(str(err), logging.ERROR)
            return False
        else:
            return True

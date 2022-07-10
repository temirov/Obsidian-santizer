from dataclasses import dataclass
from pathlib import Path

import constants
from services.file_cmp import FileCmp
from services.file_comparison_service import FileComparisonService
from utils.string_utils import StringUtils
from utils.system_utils import SystemUtils


@dataclass
class FilePair:
    left_file: Path
    right_file: Path
    glob: str
    system_utils: SystemUtils
    string_utils: StringUtils

    def __compare__(self) -> FileCmp:
        file_comparison_service = FileComparisonService(self.left_file, self.right_file, self.string_utils)
        return file_comparison_service()

    def has_glob(self) -> bool:
        return self.string_utils.has_glob_suffix(self.__remaining_file__().as_posix(), self.glob)

    def are_different(self) -> bool:
        return self.__compare__() is FileCmp.DIFFERENT

    def are_identical(self) -> bool:
        return self.__compare__() is FileCmp.IDENTICAL

    def left_contains_right(self) -> bool:
        return self.__compare__() is FileCmp.LEFT_CONTAINS_RIGHT

    def right_contains_left(self) -> bool:
        return self.__compare__() is FileCmp.RIGHT_CONTAINS_LEFT

    def delete_left(self) -> bool:
        return self.system_utils.bool_func_wrapper(self.left_file.unlink)

    def delete_right(self) -> bool:
        return self.system_utils.bool_func_wrapper(self.right_file.unlink)

    def one_file_exists(self) -> bool:
        return self.left_file.exists() ^ self.right_file.exists()

    def __remaining_file__(self) -> Path:
        if self.left_file.exists() and self.right_file.exists():
            raise RuntimeError("Both files exists")
        elif self.left_file.exists():
            return self.left_file
        elif self.right_file.exists():
            return self.right_file
        else:
            raise RuntimeError("Both files are gone!")

    def __deleted_file__(self) -> Path:
        remaining_file = self.__remaining_file__()
        for file in [self.left_file, self.right_file]:
            if file != remaining_file:
                return file
        raise RuntimeError("Must be a bug")

    def has_markdown_extension(self) -> bool:
        return self.__remaining_file__().suffix == constants.MARKDOWN_EXTENSION

    def has_no_markdown_extension(self) -> bool:
        return not self.has_markdown_extension()

    def rename(self) -> bool:
        return self.system_utils.bool_func_wrapper(self.__remaining_file__().rename, self.__deleted_file__().as_posix())

    def merge(self):
        return self.system_utils.open_merge_program(self.left_file, self.right_file, constants.VIM_MERGE_PROGRAM)

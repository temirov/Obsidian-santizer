import re
from pathlib import Path

import constants
from services.file_cmp import FileCmp
from utils.string_utils import StringUtils


class FileComparisonService:
    def __init__(self, left_file: Path, right_file: Path, string_utils: StringUtils) -> None:
        self.left_file = left_file
        self.right_file = right_file
        self.string_utils = string_utils

    @staticmethod
    def __identical_cmp__(result: str) -> bool:
        return not re.search(constants.STARTS_WITH_MINUS, result) and \
               not re.search(constants.STARTS_WITH_PLUS, result) and \
               not re.search(constants.STARTS_WITH_QUESTION_MARK, result)

    @staticmethod
    def __right_contains_left_cmp__(result: str) -> bool:
        return not re.search(constants.STARTS_WITH_MINUS, result) and \
               re.search(constants.STARTS_WITH_PLUS, result) and \
               not re.search(constants.STARTS_WITH_QUESTION_MARK, result)

    @staticmethod
    def __left_contains_right_cmp__(result: str) -> bool:
        return re.search(constants.STARTS_WITH_MINUS, result) and \
               not re.search(constants.STARTS_WITH_PLUS, result) and \
               not re.search(constants.STARTS_WITH_QUESTION_MARK, result)

    @staticmethod
    def __different_cmp__(result: str) -> bool:
        return re.search(constants.STARTS_WITH_MINUS, result) and \
               re.search(constants.STARTS_WITH_PLUS, result) and \
               not re.search(constants.STARTS_WITH_QUESTION_MARK, result)

    def __call__(self, *args, **kwargs) -> FileCmp:
        content1 = self.left_file.read_text()
        content2 = self.right_file.read_text()

        result = self.string_utils.content_diff(content1, content2)

        if self.__identical_cmp__(result):
            return FileCmp.IDENTICAL
        elif self.__right_contains_left_cmp__(result):
            return FileCmp.RIGHT_CONTAINS_LEFT
        elif self.__left_contains_right_cmp__(result):
            return FileCmp.LEFT_CONTAINS_RIGHT
        elif self.__different_cmp__(result):
            return FileCmp.DIFFERENT
        else:
            message = f"""
                result = {result}
                ====
                BAD!
                """
            raise RuntimeError(message)

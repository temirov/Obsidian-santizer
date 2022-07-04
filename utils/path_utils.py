from pathlib import Path
from typing import Iterator

import constants
from services.mime_detection_service import MimeDetectionService


class PathUtils:
    @classmethod
    def glob_path_walker(cls, folder: str, glob_pattern: str) -> Iterator[Path]:
        for path in Path(folder).rglob(glob_pattern):
            yield path

    @classmethod
    def raise_when_no_folder(cls, folder: str) -> None:
        if not cls.dir_exists(folder):
            raise RuntimeError(f"Folder {folder} does not exist")

    @classmethod
    def is_hidden(cls, path: Path) -> bool:
        return any(part.startswith('.') for part in path.parts)

    @classmethod
    def is_in_folder(cls, path: Path, folder: str) -> bool:
        return any(part == folder for part in path.parts)

    @classmethod
    def is_empty_file(cls, path: Path) -> bool:
        return path.is_file() and path.stat().st_size == 0

    @classmethod
    def is_empty_dir(cls, path: Path) -> bool:
        return path.is_dir() and not any(path.iterdir())

    @classmethod
    def is_mac_system_file(cls, path: Path) -> bool:
        return path.is_file() and path.name == constants.MAC_DS_STORE

    @classmethod
    def dir_exists(cls, value: str) -> bool:
        path = cls.as_path(value)
        return path.is_dir() and path.exists()

    @classmethod
    def is_plaintext_file(cls, path: Path) -> bool:
        file_type = cls.__get_file_type__(path)
        return path.is_file() and file_type == constants.PLAIN_TEXT_MIME_SUBTYPE

    @classmethod
    def is_pdf_file(cls, path: Path) -> bool:
        file_type = cls.__get_file_type__(path)
        return file_type == constants.PDF_MIME_SUBTYPE

    @classmethod
    def is_image_file(cls, path: Path) -> bool:
        file_type = cls.__get_file_type__(path)
        return file_type.split("/")[0] == constants.IMAGE_MIME_TYPE

    @classmethod
    def is_json_file(cls, path: Path) -> bool:
        file_type = cls.__get_file_type__(path)
        return file_type == constants.JSON_MIME_SUBTYPE

    @classmethod
    def is_application_file(cls, path: Path) -> bool:
        file_type = cls.__get_file_type__(path)
        return file_type.split("/")[0] == constants.APPLICATION_MIME_TYPE

    @classmethod
    def is_md_candidate(cls, path: Path) -> bool:
        return path.is_file() and path.suffix == constants.EMPTY_STRING and cls.is_plaintext_file(path)

    @classmethod
    def is_markup_file(cls, path: Path) -> bool:
        return path.is_file() and path.name.endswith(constants.MARKDOWN_EXTENSION)

    @classmethod
    def as_path(cls, value: str) -> Path:
        return Path(value)

    @classmethod
    def __get_file_type__(cls, path: Path) -> str:
        mime_detection_service = MimeDetectionService(path)
        return mime_detection_service()

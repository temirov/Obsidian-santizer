from pathlib import Path

from magic import magic


class MimeDetectionService:
    def __init__(self, path: Path):
        self.path = path
        self.mime_detector = magic.Magic(mime=True, uncompress=True)

    def __call__(self, *args, **kwargs) -> str:
        return self.mime_detector.from_file(self.path.as_posix())

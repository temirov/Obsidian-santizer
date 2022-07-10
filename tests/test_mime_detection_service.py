import subprocess
from pathlib import Path
from unittest import TestCase

import constants
from services.mime_detection_service import MimeDetectionService


class TestMimeDetectionService(TestCase):
    def setUp(self) -> None:
        self.expected_json_mime_type = constants.JSON_MIME_SUBTYPE
        self.expected_markdown_mime_type = constants.PLAIN_TEXT_MIME_SUBTYPE
        self.markdown_filename = "./markdown.md"
        self.json_filename = "./json.md"
        self.markdown_path = Path(self.markdown_filename)
        self.json_path = Path(self.json_filename)

    def test_markdown(self):
        mimetype = MimeDetectionService(self.markdown_path)()
        self.assertEqual(self.expected_markdown_mime_type, mimetype)

    def test_json(self):
        mimetype = MimeDetectionService(self.json_path)()
        self.assertEqual(self.expected_json_mime_type, mimetype)

    def test_mimetype(self):
        result = subprocess.check_output(['file', '-b', '--mime', self.json_path.absolute().as_posix()],
                                         universal_newlines=True)
        mimetype = result.split(";")[0]
        self.assertEqual(self.expected_json_mime_type, mimetype)

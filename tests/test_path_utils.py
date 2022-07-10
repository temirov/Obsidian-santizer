from pathlib import Path
from unittest import TestCase

from utils.path_utils import PathUtils


class TestPathUtils(TestCase):
    def setUp(self) -> None:
        self.excluded_paths = [Path("/etc/")]
        self.excluded_file = Path("/etc/hosts")

    def test_is_excluded(self):
        self.assertTrue(
            PathUtils.__is_excluded__(self.excluded_file, self.excluded_paths)
        )

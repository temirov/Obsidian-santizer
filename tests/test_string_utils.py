import textwrap
from unittest import TestCase

from utils.string_utils import StringUtils


class TestStringUtils(TestCase):
    def test_expand_and_remove_suffix(self):
        file_name = "Configure Synology Backup_SM-G998U1_Feb-06-0126-2022_1.md"
        suffix = "_SM-G998U1"
        expected = "Configure Synology Backup.md"
        actual = StringUtils.expand_and_remove_suffix(file_name, suffix)
        self.assertEqual(expected, actual)

    def test_expand_and_remove_glob_suffix(self):
        file_name = "Configure Synology Backup_SM-G998U1_Feb-06-0126-2022_1.md"
        suffix = "*_SM-G998U1_*"
        expected = "Configure Synology Backup.md"
        actual = StringUtils.expand_and_remove_suffix(file_name, suffix)
        self.assertEqual(expected, actual)

    def test_remove_substring(self):
        string = "*_SM-G998U1_*"
        expected = "_SM-G998U1_"
        actual = StringUtils.remove_substring(string, "*")
        self.assertEqual(expected, actual)

    def test_content_diff(self):
        content1 = textwrap.dedent("""
        ### Programs
        - [[Personal/Interview Prep/resources/1589474068156.623975149.png/House Maintenance|house maintenance]]
        - [[Health]]
        - [[Finance]]
        """)
        content2 = textwrap.dedent("""
        ### Programs
        - [[House Maintenance|house maintenance]]
        - [[Health]]
        - [[Finance]]
        """)
        raw_expected = textwrap.dedent("""
          ### Programs
        - - [[Personal/Interview Prep/resources/1589474068156.623975149.png/House Maintenance|house maintenance]]
        + - [[House Maintenance|house maintenance]]
          - [[Health]]
          - [[Finance]]
        """)
        expected = StringUtils.trim(raw_expected)
        actual = StringUtils.trim(StringUtils.content_diff(content1, content2))
        self.assertEqual(expected, actual)

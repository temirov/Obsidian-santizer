import re

APP_NAME = "ObsidianSanitizer"
EMPTY_STRING = ""
FILE_DATE_FORMAT = "%Y%m%d"
FILE_DATETIME_FORMAT = f"{FILE_DATE_FORMAT} %H%M%S"
LOGGING_FORMAT = '%(asctime)s %(levelname)s:%(message)s'
MAC_DS_STORE = '.DS_Store'
MAC_MERGE_PROGRAM = 'opendiff'
"""
VIMDIFF
]c: jump to the next change
[c: jump to the previous change
do: get changes from other window into the current window
dp: put the changes from current window into the other window
:xa	save all changes and close Vim
:windo set wrapped lines in both screens
"""
VIM_MERGE_PROGRAM = 'vimdiff'
STARTS_WITH_MINUS = re.compile(r'(\n|^)- ')
STARTS_WITH_PLUS = re.compile(r'(\n|^)\+ ')
STARTS_WITH_QUESTION_MARK = re.compile(r'(\n^)\? ')
MARKDOWN_EXTENSION = '.md'
ALL_FILES = '*'
IMAGE_MIME_TYPE = "image"
APPLICATION_MIME_TYPE = "application"
PLAIN_TEXT_MIME_SUBTYPE = "text/plain"
JSON_MIME_SUBTYPE = f"{APPLICATION_MIME_TYPE}/json"
PDF_MIME_SUBTYPE = f"{APPLICATION_MIME_TYPE}/pdf"
MAC_OS = "Darwin"
UNIX_CR = "\n"
OBSIDIAN_RESOURCE_FOLDER = "resources"
OBSIDIAN_SUSPICIOUS_FOLDER = "sus"

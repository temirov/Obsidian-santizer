from services.file_cmp import FileCmp
from services.file_pair import FilePair
from services.proceeding_final_machine import ProceedingFinalMachine


class MarkdownRenamingService:
    def __init__(self, file_pair: FilePair) -> None:
        self.file_pair = file_pair
        self.final_state = FileCmp.ONE_FILE_CORRECT_EXTENSION
        self.initial_state = FileCmp.TBD
        self.transitions = [
            {'trigger': 'proceed', 'source': FileCmp.IDENTICAL, 'dest': FileCmp.ONE_FILE, 'before': 'delete_left'},
            {'trigger': 'proceed', 'source': FileCmp.LEFT_CONTAINS_RIGHT, 'dest': FileCmp.ONE_FILE,
             'before': 'delete_right'},
            {'trigger': 'proceed', 'source': FileCmp.RIGHT_CONTAINS_LEFT, 'dest': FileCmp.ONE_FILE,
             'before': 'delete_left'},
            {'trigger': 'proceed', 'source': FileCmp.ONE_FILE, 'dest': FileCmp.ONE_FILE_INCORRECT_EXTENSION,
             'conditions': 'has_no_markdown_extension'},
            {'trigger': 'proceed', 'source': FileCmp.ONE_FILE, 'dest': FileCmp.ONE_FILE_GLOB_NAME,
             'conditions': 'has_glob'},
            {'trigger': 'proceed', 'source': FileCmp.ONE_FILE, 'dest': FileCmp.ONE_FILE_CORRECT_EXTENSION,
             'conditions': 'has_markdown_extension'},
            {'trigger': 'proceed', 'source': FileCmp.ONE_FILE_INCORRECT_EXTENSION,
             'dest': FileCmp.ONE_FILE_CORRECT_EXTENSION, 'before': 'rename'},
            {'trigger': 'proceed', 'source': FileCmp.ONE_FILE_GLOB_NAME,
             'dest': FileCmp.ONE_FILE, 'before': 'rename_glob'},
            {'trigger': 'proceed', 'source': FileCmp.DIFFERENT, 'dest': FileCmp.TBD, 'before': 'merge'},
            {'trigger': 'proceed', 'source': FileCmp.TBD, 'dest': FileCmp.ONE_FILE, 'conditions': 'one_file_exists'},
            {'trigger': 'proceed', 'source': FileCmp.TBD, 'dest': FileCmp.IDENTICAL, 'conditions': 'are_identical'},
            {'trigger': 'proceed', 'source': FileCmp.TBD, 'dest': FileCmp.LEFT_CONTAINS_RIGHT,
             'conditions': 'left_contains_right'},
            {'trigger': 'proceed', 'source': FileCmp.TBD, 'dest': FileCmp.RIGHT_CONTAINS_LEFT,
             'conditions': 'right_contains_left'},
            {'trigger': 'proceed', 'source': FileCmp.TBD, 'dest': FileCmp.DIFFERENT, 'conditions': 'are_different'}
        ]

    def __call__(self, *args, **kwargs):
        processing_final_machine = ProceedingFinalMachine(model=self.file_pair, transitions=self.transitions,
                                                          states=FileCmp, initial_state=self.initial_state,
                                                          final_state=self.final_state)
        processing_final_machine()

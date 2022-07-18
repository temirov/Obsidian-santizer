from pathlib import Path

from transitions.extensions import GraphMachine

from logger.logger import Logger
from services.file_cmp import FileCmp
from services.file_pair import FilePair
from services.markdown_renaming_service import MarkdownRenamingService
from utils.string_utils import StringUtils
from utils.system_utils import SystemUtils


def main():
    logger = Logger()
    string_utils = StringUtils()
    system_utils = SystemUtils(logger)
    model = FilePair(glob="*",
                     left_file=Path("/etc/hosts"),
                     right_file=Path("/etc/hosts"),
                     system_utils=system_utils,
                     string_utils=string_utils)
    markdown_renaming_service = MarkdownRenamingService(model)

    machine = GraphMachine(model=model,
                           states=FileCmp,
                           transitions=markdown_renaming_service.transitions,
                           initial=FileCmp.TBD,
                           title="Markdown Renaming FSM",
                           show_conditions=True,
                           show_state_attributes=True,
                           show_auto_transitions=False)

    # draw the whole graph ...
    machine.get_graph().draw('fsm_diagram.png', prog='dot')


if __name__ == '__main__':
    main()

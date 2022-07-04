from enum import Enum
from typing import Union

from transitions import Machine


class ProceedingFinalMachine:
    def __init__(self, model: object, states: Enum, initial_state: Enum, final_state: Enum,
                 transitions: list[dict[str, Union[str, Enum]]]) -> None:
        self.model = model
        self.states = states
        self.final_state = final_state
        self.initial_state = initial_state
        self.transitions = transitions

        self.__validate__()
        self.machine = Machine(model=self.model, states=self.states, transitions=self.transitions,
                               initial=self.initial_state)

    def __validate__(self):
        if not all(transition['trigger'] == 'proceed' for transition in self.transitions):
            raise RuntimeError("trigger must be called 'proceed'")

    def __call__(self, *args, **kwargs):
        while self.model.state is not self.final_state:
            self.model.proceed()

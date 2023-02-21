# coding: utf-8

from generator.internal_lib.list import strlist_to_str, flatten
from generator.metaprog.my_enum import PromptChoiceEnum
from generator.sys.error import terminate
import generator.config.rules.dev.debugger as DEBUGGER_CONFIG

from enum import Enum
from typing import List


class ConfirmChoice(PromptChoiceEnum):
    ACCEPT = ["y", "yes"]
    REJECT = ["n", "no"]


def _generate_choices_indicator(enum: Enum, defaut_enum_value = None):
    confirm_choices = list(enum)
    if defaut_enum_value is None:
        default_choice_index = -1
    else:
        default_choice_index = confirm_choices.index(defaut_enum_value)

    choices_indicator: List[str] = []
    default_choice_indicator: str = ''
    for index, choice in enumerate(confirm_choices):
        if index == default_choice_index:
            default_choice_indicator = choice.value[0].upper()
        else:
            choices_indicator.append(choice.value[0])

    if default_choice_indicator:
        choices_indicator.insert(0, default_choice_indicator)
    choices_indicator_str = strlist_to_str(choices_indicator, '/')

    return choices_indicator_str


def choice_prompt(msg: str, enum: PromptChoiceEnum, default_confirm = None):
    choices: list = flatten(enum.values())
    choices_indicator: str = _generate_choices_indicator(enum, default_confirm)
    user_input: str = ''

    while True:
        print(msg)
        user_input: str = input(f"Continue? [{choices_indicator}] ").lower().strip()
        if user_input in choices:
            break
        elif default_confirm is not None and user_input == '':
            break

    if user_input == '':
        return default_confirm

    confirm_choices = list(enum)
    for index, choice in enumerate(confirm_choices):
        if user_input in choice.value:
            return choice

    terminate(DEBUGGER_CONFIG.BUGTRACKER_MSG)

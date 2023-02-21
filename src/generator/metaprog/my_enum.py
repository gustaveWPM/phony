# coding: utf-8

from enum import Enum


class PromptChoiceEnum(Enum):

    @classmethod
    def values(cls) -> list:
        return list(map(lambda c: c.value, cls))

    # * ... see: https://stackoverflow.com/questions/29503339/how-to-get-all-values-from-python-enum-class

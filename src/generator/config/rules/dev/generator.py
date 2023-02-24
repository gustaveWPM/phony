# coding: utf-8


from generator.metaprog.types import Schema


DB_ENTRIES_CHUNK_SIZE = 50000                   # * ... Default value is `50000`
DISABLE_MULTITHREADING = False                  # * ... Default value is `False`
ALLOW_DUPLICATES = False                        # * ... Default value is `False`
DISABLE_SHUFFLE = False                         # * ... Default value is `False`

DEBUG_MODE = True                              # * ... Default value is `False`


"""

⬇️ UNSAFE MODE ⬇️

"""


UNSAFE = False                                  # * ... Default value is `False`

FORCED_OPERATOR_CODES: list = []                # * ... Default value is `[]`

AUTOCONFIRM_PROMPTS = Schema({
    "CONFIGURATION_ERROR": False                # * ... Default value is `False`
})

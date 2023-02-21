# coding: utf-8


from generator.metaprog.types import Schema


DB_ENTRIES_CHUNK_SIZE = 5000                    # * ... Default value is `5000`
DISABLE_MULTITHREADING = False                  # * ... Default value is `False`
ALLOW_DUPLICATES = False                        # * ... Default value is `False`

DEBUG_MODE = False                              # * ... Default value is `False`


"""

⬇️ UNSAFE MODE ⬇️

"""


UNSAFE = False                                  # * ... Default value is `False`
DISABLE_SMART_RELOAD = False                    # * ... Default value is `False`
FORCE_VERY_FIRST_ITERATION = False              # * ... Default value is `False`

FORCED_VERY_FIRST_ITERATION_VALUE: str = "0"    # * ... Default value is `"0"`
FORCED_RANGE_START: int = -1                    # * ... Default value is `-1`
FORCED_RANGE_END: int = -1                      # * ... Default value is `-1`
FORCED_OPERATOR_CODES: list = []                # * ... Default value is `[]`

AUTOCONFIRM_PROMPTS = Schema({
    "CONFIGURATION_ERROR": False                # * ... Default value is `False`
})

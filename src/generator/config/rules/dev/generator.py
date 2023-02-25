# coding: utf-8


from generator.metaprog.types import Schema


DISABLE_SHUFFLE = False                         # * ... Default value is `False`
MAX_DB_CHUNKS_RECORDS_BEFORE_SHUFFLE = 3        # * ... Default value is `3`. Set it to `0` to disable this feature.
DISABLE_MULTITHREADING = False                  # * ... Default value is `False`
DB_ENTRIES_CHUNK_SIZE = 50000                   # * ... Default value is `50000`
DB_ENTRIES_CHUNK_SIZE_RANDOM_DELTA = 49000      # * ... Default value is `49000`. Set it to `0` to disable this feature.
ALLOW_DUPLICATES = False                        # * ... Default value is `False`

DEBUG_MODE = True                              # * ... Default value is `False`


"""

⬇️ UNSAFE MODE ⬇️

"""


UNSAFE = False                                  # * ... Default value is `False`

FORCED_OPERATOR_CODES: list = []                # * ... Default value is `[]`

AUTOCONFIRM_PROMPTS = Schema({})                # * ... Unused feature atm

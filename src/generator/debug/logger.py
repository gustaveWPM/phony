# coding: utf-8


from generator.debug.vocab import VOCAB
from generator.metaprog.types import Void


def debug_logger(msg_key: str, value: any = '') -> Void:
    colon = ": " if value != '' else ''
    print(f"{VOCAB['DEBUG_PREFIX']} {VOCAB['DEBUG_MSG'][msg_key]}{colon}{value}.")

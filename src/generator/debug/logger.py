# coding: utf-8

from generator.metaprog.types import Void
from generator.debug.vocab import VOCAB

def debug_logger(msg_key: str, value: any = '') -> Void:
    colon: str = ": " if value != '' else ''
    print(f"{VOCAB['DEBUG_PREFIX']} {VOCAB['DEBUG_MSG'][msg_key]}{colon}{value}.")

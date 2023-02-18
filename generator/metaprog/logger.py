# coding: utf-8

from metaprog.aliases import Void
from metaprog.vocab import VOCAB

def debug_logger(msg_key: str, value: any) -> Void:
    print(f"{VOCAB['DEBUG_PREFIX']} {VOCAB['DEBUG_MSG'][msg_key]}: {value}")

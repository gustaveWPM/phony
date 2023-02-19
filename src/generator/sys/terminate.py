# coding: utf-8

import sys


def terminate(msg: str = '', exit_code: int = 1):
    if msg:
        if exit_code == 1:
            print(msg, file=sys.stderr)
        else:
            print(msg)
    exit(exit_code)

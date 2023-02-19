# coding: utf-8

import sys


def print_on_stderr(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def terminate(msg: str = '', exit_code: int = 1):
    if msg:
        if exit_code == 1:
            print_on_stderr(msg)
        else:
            print(msg)
    exit(exit_code)

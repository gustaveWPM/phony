# coding: utf-8

from functools import reduce

def uniq(l: list) -> list:
    l_uniq = reduce(lambda re, x: re+[x] if x not in re else re, l, [])
    return l_uniq

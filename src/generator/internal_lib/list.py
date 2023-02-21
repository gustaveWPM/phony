# coding: utf-8


from functools import reduce
from typing import List


def flatten(l: list) -> list:
    return [item for sublist in l for item in sublist]

    # * ... see: https://stackoverflow.com/questions/952914/how-do-i-make-a-flat-list-out-of-a-list-of-lists


def uniq(l: list) -> list:
    l_uniq = reduce(lambda re, x: re+[x] if x not in re else re, l, [])
    return l_uniq

    # * ... see: https://www.geeksforgeeks.org/python-get-unique-values-list/


def reverse(l: list) -> list:
    rev_l = l[::-1]
    return rev_l


def to_strlist(l: list) -> list:
    l_to_strlist: List[str] = [str(c) for c in l]
    return l_to_strlist


def strlist_to_str(l: List[str], separator: str = '') -> str:
    l_to_str: str = separator.join(l)
    return l_to_str


def list_to_str(l: list) -> str:
    l_to_strlist = to_strlist(l)
    l_to_str = strlist_to_str(l_to_strlist)
    return l_to_str

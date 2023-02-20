# coding: utf-8

from typing import List
from functools import reduce


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


def strlist_to_str(l: List[str]) -> str:
    l_to_str: str = ''.join(l)
    return l_to_str


def list_to_str(l: list) -> str:
    l_to_strlist = to_strlist(l)
    l_to_str = strlist_to_str(l_to_strlist)
    return l_to_str

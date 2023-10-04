# coding: utf-8


from typing import List


def flatten(l: list) -> list:
    return [item for sublist in l for item in sublist]

    # * ... see: https://stackoverflow.com/questions/952914/how-do-i-make-a-flat-list-out-of-a-list-of-lists


def uniq(l: list) -> list:
    return list(dict.fromkeys(l))

    # * ... see: https://stackoverflow.com/questions/1653970/does-python-have-an-ordered-set


def reverse(l: list) -> list:
    rev_l = l[::-1]
    return rev_l


def to_strlist(l: list) -> list:
    l_to_strlist: List[str] = [str(v) for v in l]
    return l_to_strlist


def strlist_to_str(l: List[str], separator: str = '') -> str:
    l_to_str: str = separator.join(l)
    return l_to_str


def list_to_str(l: list) -> str:
    l_to_strlist = to_strlist(l)
    l_to_str = strlist_to_str(l_to_strlist)
    return l_to_str

# coding: utf-8

from itertools import groupby


def str_groupby(s: str) -> dict:
    groups = groupby(s)
    result = [(label, sum(1 for _ in group)) for label, group in groups]
    return result

# * ... lol: https://stackoverflow.com/questions/34443946/count-consecutive-characters

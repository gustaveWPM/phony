# coding: utf-8


from itertools import groupby


def str_groupby(s: str) -> list:
    groups = groupby(s)
    result = [(label, sum(1 for _ in group)) for label, group in groups]
    return result

    # * ... see: https://stackoverflow.com/questions/34443946/count-consecutive-characters

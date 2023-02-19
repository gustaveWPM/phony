# coding: utf-8

import generator.config.rules.dev.generator as DEV
from typing import Optional, List
from generator.config.rules.absolute_getters.generator import get_ndigits
from generator.internal_lib.list import reverse, list_to_str
from generator.config.rules.generator import GENERATOR as CONF


def compute_range_len(op_code: str) -> int:
    ndigits: int = get_ndigits()
    range_len: int = ndigits - len(op_code)
    return range_len


def compute_range_start(metadatas: Optional[dict], cur_op_code: str, magnitude: int) -> int:
    first_iteration: int = 0
    head_max_zeros = CONF["HEAD_MAX_ZEROS"]
    block_len: int = compute_range_len(cur_op_code)

    if (DEV.FORCED_FIRST_ITERATION >= 0 and DEV.UNSAFE):
        first_iteration = DEV.FORCED_FIRST_ITERATION
        return first_iteration

    if (DEV.DISABLE_SMART_RELOAD):
        first_iteration = 0
        return first_iteration

    if (metadatas is not None):
        first_iteration = int(metadatas["phone_number_suffix"]) + 1
        return first_iteration

    if (DEV.FORCE_VERY_FIRST_ITERATION_VALUE and DEV.UNSAFE):
        first_iteration = int(DEV.FORCED_VERY_FIRST_ITERATION)
        return first_iteration

    if (head_max_zeros >= block_len):
        return -1
    pos: int = head_max_zeros
    str_base = '0' * block_len
    first_iteration_str = str_base[:pos] + '1' + str_base[pos + 1:]
    first_iteration = int(first_iteration_str)

    if (head_max_zeros == 0 and first_iteration < magnitude):
        first_iteration = magnitude

    return first_iteration


def _do_compute_last_iter_tail(
    trail_len: int,
    head: str,
    same_digit_threshold: int
) -> int:
    trail: str = ''
    current_digit: int = 9

    trail_elements: List[int] = [8]
    trail_len -= 1
    while (trail_len > 0):
        current_digit_in_trail_occurrences: int = trail_elements.count(current_digit);
        current_digit_in_head_occurrences: int = head.count(str(current_digit))
        total_cur_digit: int = current_digit_in_trail_occurrences + current_digit_in_head_occurrences
        
        if (total_cur_digit >= same_digit_threshold):
            current_digit -= 1
            if current_digit < 0:
                raise RuntimeError("You're not funny at all! Do you even know what you are doing with the config files?")
            continue

        trail_elements.append(current_digit)
        trail_len -= 1
    trail = list_to_str(trail_elements)
    last_iter_str: str = head + trail
    last_iteration = int(last_iter_str) + 1
    return last_iteration


def _do_compute_consecutive_nines_at_op_code_tail(op_code: str) -> int:
    rev_op_code = reverse(op_code)
    consecutive_nines_at_op_code_tail: int = 0

    for c in rev_op_code:
        if (c == '9'):
            consecutive_nines_at_op_code_tail += 1
        else:
            break

    return consecutive_nines_at_op_code_tail


def _do_compute_last_iter(op_code: str, block_len: int) -> int:
    last_iteration: int = -1
    same_digit_threshold: int = CONF["SAME_DIGIT_THRESHOLD"]
    same_consecutive_digit_threshold: int = CONF["CONSECUTIVE_SAME_DIGIT_THRESHOLD"]

    consecutive_nines_at_op_code_tail: int = _do_compute_consecutive_nines_at_op_code_tail(op_code)

    # {ToDo} Move (and enhance to fit all digit cases) this logic in the validator
    if consecutive_nines_at_op_code_tail > same_consecutive_digit_threshold:
        raise ValueError(f"Too much '9' at the tail of your op code ({op_code}). Check your CONSECUTIVE_SAME_DIGIT_THRESHOLD in your fine-tune config ({same_consecutive_digit_threshold}).")

    head_appended_nines: str = '9' * (same_consecutive_digit_threshold - consecutive_nines_at_op_code_tail)
    head: str = op_code + head_appended_nines
    trail_len: int = block_len - len(head_appended_nines)

    if trail_len > 0:
        last_iteration = _do_compute_last_iter_tail(trail_len, head, same_digit_threshold)
    return last_iteration


def compute_range_end(ndigits: int, op_code: str) -> int:
    last_iteration: int = 0
    block_len: int = compute_range_len(op_code)

    # {ToDo} Move this logic in the validator
    if block_len < 0:
        raise ValueError(f"Bigger operator code len ({op_code}) than NDIGITS ({ndigits}).")

    if (DEV.FORCED_LAST_ITERATION >= 0 and DEV.UNSAFE):
        last_iteration = DEV.FORCED_LAST_ITERATION
        return last_iteration

    if block_len == 0:
        last_iteration = int(op_code) + 1
        return last_iteration

    last_iteration = _do_compute_last_iter(op_code, block_len)
    return last_iteration

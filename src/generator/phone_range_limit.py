# coding: utf-8

import generator.config.rules.dev.generator as DEV_CONFIG
from generator.config.rules.generator import GENERATOR as GENERATOR_CONFIG
import generator.config.rules.dev.debugger as DEBUGGER_CONFIG
from generator.config.absolute_getters.generator import get_ndigits
from generator.internal_lib.list import reverse, list_to_str
from generator.sys.error import terminate

from typing import Optional, List


def compute_range_len(op_code: str) -> int:
    ndigits: int = get_ndigits()
    range_len: int = ndigits - len(op_code)
    return range_len


def compute_range_start(metadatas: Optional[dict], cur_op_code: str, magnitude: int) -> int:
    range_start: int = 0
    last_block_head_max_zeros = GENERATOR_CONFIG["LAST_BLOCK_HEAD_MAX_ZEROS"]
    block_len: int = compute_range_len(cur_op_code)

    if DEV_CONFIG.FORCE_VERY_FIRST_ITERATION and DEV_CONFIG.UNSAFE:
        range_start = int(DEV_CONFIG.FORCED_VERY_FIRST_ITERATION_VALUE)
        return range_start

    if DEV_CONFIG.FORCED_RANGE_START >= 0 and DEV_CONFIG.UNSAFE:
        range_start = DEV_CONFIG.FORCED_RANGE_START
        return range_start

    if metadatas is not None and not DEV_CONFIG.DISABLE_SMART_RELOAD:
        range_start = int(metadatas["phone_number_suffix"]) + 1
        return range_start

    if last_block_head_max_zeros >= block_len:
        return 0

    pos: int = last_block_head_max_zeros
    str_base = '0' * block_len
    range_start_str = str_base[:pos] + '1' + str_base[pos + 1:]
    range_start = int(range_start_str)

    if last_block_head_max_zeros == 0 and range_start < magnitude:
        range_start = magnitude

    return range_start


def _do_compute_range_end_tail(
    trail_len: int,
    head: str,
    head_appended_nines: str,
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
        
        if total_cur_digit >= same_digit_threshold:
            current_digit -= 1
            if current_digit < 0:
                terminate(DEBUGGER_CONFIG.BUGTRACKER_MSG)
            continue

        trail_elements.append(current_digit)
        trail_len -= 1
    trail = list_to_str(trail_elements)
    range_end_str: str = head_appended_nines + trail
    range_end = int(range_end_str) + 1
    return range_end


def _do_compute_consecutive_nines_at_op_code_tail(op_code: str) -> int:
    rev_op_code = reverse(op_code)
    consecutive_nines_at_op_code_tail: int = 0

    for c in rev_op_code:
        if c == '9':
            consecutive_nines_at_op_code_tail += 1
        else:
            break

    return consecutive_nines_at_op_code_tail


def _do_compute_range_end(op_code: str, block_len: int) -> int:
    range_end: int = 0
    same_digit_threshold: int = GENERATOR_CONFIG["SAME_DIGIT_THRESHOLD"]
    same_consecutive_digit_threshold: int = GENERATOR_CONFIG["CONSECUTIVE_SAME_DIGIT_THRESHOLD"]

    consecutive_nines_at_op_code_tail: int = _do_compute_consecutive_nines_at_op_code_tail(op_code)
    head_appended_nines: str = '9' * (same_consecutive_digit_threshold - consecutive_nines_at_op_code_tail)
    head: str = op_code + head_appended_nines
    trail_len: int = block_len - len(head_appended_nines)

    if trail_len > 0:
        range_end = _do_compute_range_end_tail(trail_len, head, head_appended_nines, same_digit_threshold)
    return range_end


def compute_range_end(op_code: str) -> int:
    range_end: int = 0
    block_len: int = compute_range_len(op_code)

    if DEV_CONFIG.FORCED_RANGE_END >= 0 and DEV_CONFIG.UNSAFE:
        range_end = DEV_CONFIG.FORCED_RANGE_END
        return range_end

    if block_len == 0:
        range_end = int(op_code) + 1
        return range_end

    range_end = _do_compute_range_end(op_code, block_len)
    return range_end

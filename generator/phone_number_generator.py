# coding: utf-8

from typing import Optional, List
from metaprog.logger import debug_logger as DebugLogger
from metaprog.vocab import VOCAB
from metaprog.aliases import *
from obj.contracts.prefix_data import PrefixData
import config.rules.dev.generator as DEV
from config.rules.generator import GENERATOR as CONF
import config.validator as config_validator
import database.db as db


def _reject_phone_number_suffix(operator_code: str, phone_number_suffix: str) -> bool:
    head_max_zeros: int = CONF["HEAD_MAX_ZEROS"]
    same_digit_threshold: int = CONF["SAME_DIGIT_THRESHOLD"]
    same_consecutive_digit_threshold: int = CONF["CONSECUTIVE_SAME_DIGIT_THRESHOLD"]
    digits: str = "0123456789"
    whole_phone_number: str = operator_code + phone_number_suffix
    pattern: str = ''

    if (phone_number_suffix.startswith('0' * (head_max_zeros + 1))):
        return True
    for digit in digits:
        if (whole_phone_number.count(digit) > same_digit_threshold):
            return True
        if (same_consecutive_digit_threshold > 0):
            pattern = digit * (same_consecutive_digit_threshold + 1)
            if pattern in whole_phone_number:
                return True
    return False


def _append_heading_zeros(number: int, ndigits: int, magnitude: int) -> str:
    number_as_string: str = str(number)
    if (number >= magnitude):
        return number_as_string
    number_len: int = len(number_as_string)
    number_of_zeros_to_append: int = abs(ndigits - number_len)
    phone_suffix: str = '0' * number_of_zeros_to_append + number_as_string
    return phone_suffix


# {ToDo} Refactor this (hhhrrrnnnggllllhhh)
def _compute_last_iter(ndigits: int, op_code: str) -> int:
    last_iteration: int = 0
    computed_ndigits: int = ndigits - len(op_code)
    same_consecutive_digit_threshold: int = CONF["CONSECUTIVE_SAME_DIGIT_THRESHOLD"]
    same_digit_threshold: int = CONF["SAME_DIGIT_THRESHOLD"]

    if computed_ndigits < 0:
        raise ValueError(f"Bigger operator code len ({op_code}) than NDIGITS ({ndigits}).")

    if (DEV.FORCED_LAST_ITERATION >= 0 and DEV.UNSAFE):
        last_iteration = DEV.FORCED_LAST_ITERATION
        return last_iteration

    if computed_ndigits == 0:
        last_iteration = int(op_code) + 1
        return last_iteration

    rev_op_code = op_code[::-1]
    consecutive_nines_at_op_code_tail: int = 0

    for c in rev_op_code:
        if (c == '9'):
            consecutive_nines_at_op_code_tail += 1
        else:
            break

    if consecutive_nines_at_op_code_tail > same_consecutive_digit_threshold:
        raise ValueError(f"Too much '9' at the tail of your op code ({op_code}). Check your CONSECUTIVE_SAME_DIGIT_THRESHOLD in your fine-tune config ({same_consecutive_digit_threshold}).")

    head_appended_nines: str = '9' * (same_consecutive_digit_threshold - consecutive_nines_at_op_code_tail)
    head = op_code + head_appended_nines
    trail: str = ''
    trail_len: int = computed_ndigits - len(head_appended_nines)

    if trail_len > 0:
        current_digit = 9
        trail_elements = [8]

        while (trail_len > 1):
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
        trail_elements_to_s_list = [str(c) for c in trail_elements]
        suffix = ''.join(trail_elements_to_s_list)
        last_iter_str: str = head_appended_nines + trail + suffix

    last_iteration = int(last_iter_str) + 1
    return last_iteration


def _compute_first_iter(metadatas: Optional[dict], ndigits: int, max_head_zeros: int) -> int:
    first_iteration: int = 0

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

    if (max_head_zeros >= ndigits):
        return -1
    pos: int = max_head_zeros
    str_base = '0' * ndigits
    first_iteration_str = str_base[:pos] + '1' + str_base[pos + 1:]
    first_iteration = int(first_iteration_str)
    return first_iteration


def _do_generate_loop(ndigits: int, prefix_data: PrefixData, op_codes: List[str], metadatas: Optional[dict]):
    country_code: str = ''
    head_max_zeros: int = 0
    country_code = prefix_data.country_code()
    head_max_zeros = CONF["HEAD_MAX_ZEROS"]

    for cur_operator_code in op_codes:
        prefix: str = country_code + cur_operator_code
        computed_ndigits: int = ndigits - len(cur_operator_code)
        magnitude: int = 10 ** (computed_ndigits - 1)
        last_iteration: int = _compute_last_iter(ndigits, cur_operator_code)
        first_iteration: int = _compute_first_iter(metadatas, computed_ndigits, head_max_zeros)

        if first_iteration == -1 or last_iteration == -1:
            break

        if (head_max_zeros == 0 and first_iteration < magnitude):
            first_iteration = magnitude

        for current_iteration in range(first_iteration, last_iteration):
            cur_phone_number_suffix: str = _append_heading_zeros(
                current_iteration, computed_ndigits, magnitude)

            if (not _reject_phone_number_suffix(cur_operator_code, cur_phone_number_suffix)):
                cur_phone_number: str = prefix + cur_phone_number_suffix
                db.save_phone_number(cur_phone_number, country_code,
                                     cur_operator_code, cur_phone_number_suffix)
                if (DEV.DEBUG_MODE):
                    DebugLogger("GENERATED_PHONE_NUMBER", cur_phone_number)
"""             else:
                cur_phone_number: str = prefix + cur_phone_number_suffix
                print(f"Rejected: {cur_phone_number}")
"""


def _do_generate(ndigits: int, prefix_data: PrefixData, metadatas: dict) -> Void:
    op_codes_a: List[str] = []
    op_codes_b: List[str] = []

    if prefix_data.start_with_desk():
        op_codes_a = prefix_data.operator_desk_codes()
        op_codes_b = prefix_data.operator_mobile_codes()
    else:
        op_codes_a = prefix_data.operator_mobile_codes()
        op_codes_b = prefix_data.operator_desk_codes()

    _do_generate_loop(ndigits, prefix_data, op_codes_a, metadatas)
    _do_generate_loop(ndigits, prefix_data, op_codes_b, metadatas)


def _slice_operator_codes(metadatas: Optional[dict], prefix_data: PrefixData) -> Void:
    if (metadatas is None):
        return
    needle: str = metadatas["phone_number_operator_code"]

    operator_desk_codes: List[str] = prefix_data.operator_desk_codes()
    operator_mobile_codes: List[str] = prefix_data.operator_mobile_codes()

    if needle in operator_desk_codes:
        index: int = operator_desk_codes.index(needle)
        prefix_data.operator_desk_codes(operator_desk_codes[index:])
        prefix_data.start_with_desk(True)

    if needle in operator_mobile_codes:
        index: int = operator_mobile_codes.index(needle)
        prefix_data.operator_mobile_codes(operator_mobile_codes[index:])
        prefix_data.start_with_desk(False)


def _skip_generation(data: Optional[dict]) -> bool:
    if (data is None):
        return False
    return db.is_finite_collection(data)


def _run_phone_numbers_generator() -> Void:
    prefix_data: PrefixData = CONF["PREFIX_DATA"]
    ndigits: int = CONF["NDIGITS"]
    reload_metas: dict = db.retrieve_last_saved_phone_metadatas()

    if (_skip_generation(reload_metas)):
        print(VOCAB["WARNING_MSG"]["ALREADY_REACHED_FINAL_EXIT_POINT"])
        return

    if (DEV.FORCED_OPERATOR_CODES and DEV.UNSAFE):
        prefix_data.force_operator_codes(DEV.FORCED_OPERATOR_CODES)
    else:
        _slice_operator_codes(reload_metas, prefix_data)

    _do_generate(ndigits, prefix_data, reload_metas)
    db.append_finite_collection_indicator()
    print(VOCAB["SUCCESS_MSG"]["REACHED_FINAL_EXIT_POINT"])


def run() -> Void:
    config_validator.check_config(CONF)
    _run_phone_numbers_generator()

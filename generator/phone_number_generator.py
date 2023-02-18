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
            pattern = digit * same_consecutive_digit_threshold
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


def _compute_max_iter(ndigits: int, op_code: str) -> int:
    max_iteration: int = 0
    computed_ndigits: int = ndigits - len(op_code)

    if (DEV.FORCED_MAX_ITERATION != -1 and DEV.UNSAFE):
        max_iteration = DEV.FORCED_MAX_ITERATION
    else:
        t: int = CONF["SAME_DIGIT_THRESHOLD"]
        n: int = computed_ndigits
        max_iteration = int('9' * (t + 1) + '0' * abs(n - t)) // 10 + 1
    return max_iteration


def _do_generate_loop(ndigits: int, prefix_data: PrefixData, first_iteration: int, op_codes: List[str]):
    country_code: str = ''
    head_max_zeros: int = 0
    country_code = prefix_data.country_code()
    head_max_zeros = CONF["HEAD_MAX_ZEROS"]

    for cur_operator_code in op_codes:
        prefix: str = country_code + cur_operator_code
        computed_ndigits: int = ndigits - len(cur_operator_code)
        magnitude: int = 10 ** (computed_ndigits - 1)
        max_iteration: int = _compute_max_iter(ndigits, cur_operator_code)

        if (head_max_zeros == 0 and first_iteration < magnitude):
            first_iteration = magnitude

        for current_iteration in range(first_iteration, max_iteration):
            cur_phone_number_suffix: str = _append_heading_zeros(
                current_iteration, computed_ndigits, magnitude)

            if (not _reject_phone_number_suffix(cur_operator_code, cur_phone_number_suffix)):
                cur_phone_number: str = prefix + cur_phone_number_suffix
                db.save_phone_number(cur_phone_number, country_code,
                                  cur_operator_code, cur_phone_number_suffix)
                if (DEV.DEBUG_MODE):
                    DebugLogger("GENERATED_PHONE_NUMBER", cur_phone_number)
            # else:
            #    cur_phone_number: str = prefix + cur_phone_number_suffix
            #    print(f"Rejected: {cur_phone_number}")


def _do_generate(ndigits: int, prefix_data: PrefixData, first_iteration: int) -> Void:
    op_codes_a: List[str] = []
    op_codes_b: List[str] = []

    if prefix_data.start_with_desk():
        op_codes_a = prefix_data.operator_desk_codes()
        op_codes_b = prefix_data.operator_mobile_codes()
    else:
        op_codes_a = prefix_data.operator_mobile_codes()
        op_codes_b = prefix_data.operator_desk_codes()

    _do_generate_loop(ndigits, prefix_data, first_iteration, op_codes_a)
    _do_generate_loop(ndigits, prefix_data, first_iteration, op_codes_b)


def _compute_first_iteration_value(metadatas: dict) -> int:
    first_iteration: int = 0
    if (DEV.DISABLE_SMART_RELOAD):
        first_iteration = 0
        return first_iteration
    if (DEV.FORCE_VERY_FIRST_ITERATION_VALUE and DEV.UNSAFE):
        first_iteration = int(DEV.FORCED_VERY_FIRST_ITERATION)
    else:
        first_iteration = 0
    if (metadatas is None):
        return first_iteration
    first_iteration = int(metadatas["phone_number_suffix"]) + 1
    return first_iteration


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
    first_iteration: int = 0
    prefix_data: PrefixData = CONF["PREFIX_DATA"]
    ndigits: int = CONF["NDIGITS"]
    reload_metas: dict = db.retrieve_last_saved_phone_metadatas()

    if (_skip_generation(reload_metas)):
        print(VOCAB["WARNING_MSG"]["ALREADY_REACHED_FINAL_EXIT_POINT"])
        return

    if (DEV.FORCED_FIRST_ITERATION != -1 and DEV.UNSAFE):
        first_iteration = DEV.FORCED_FIRST_ITERATION
    else:
        first_iteration = _compute_first_iteration_value(reload_metas)

    if (DEV.FORCED_OPERATOR_CODES and DEV.UNSAFE):
        prefix_data.force_operator_codes(DEV.FORCED_OPERATOR_CODES)
    else:
        _slice_operator_codes(reload_metas, prefix_data)

    _do_generate(ndigits, prefix_data, first_iteration)
    db.append_finite_collection_indicator()
    print(VOCAB["SUCCESS_MSG"]["REACHED_FINAL_EXIT_POINT"])


def run() -> Void:
    config_validator.check_config(CONF)
    _run_phone_numbers_generator()

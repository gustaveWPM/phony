# coding: utf-8

from typing import Optional
from metaprog.logger import debug_logger as DebugLogger
from metaprog.vocab import VOCAB
from metaprog.aliases import *
from obj.contracts.prefix_data import PrefixData
import config.rules.dev.generator as DEV
from config.rules.generator import GENERATOR as CONF
import config.validator as config_validator
import database.db as db


def _reject_phone_number_suffix(operator_code: str, phone_number_suffix: str) -> bool:
    head_max_zeros = CONF["HEAD_MAX_ZEROS"]
    same_digit_threshold = CONF["SAME_DIGIT_THRESHOLD"]
    same_consecutive_digit_threshold = CONF["CONSECUTIVE_SAME_DIGIT_THRESHOLD"]
    digits = "0123456789"
    whole_phone_number = operator_code + phone_number_suffix

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
    number_as_string = str(number)
    if (number >= magnitude):
        return number_as_string
    number_len = len(number_as_string)
    number_of_zeros_to_append = abs(ndigits - number_len)
    phone_suffix = '0' * number_of_zeros_to_append + number_as_string
    return phone_suffix


def _do_generate(ndigits: int, prefix_data: PrefixData, first_iteration: int) -> Void:
    if (DEV.FORCED_MAX_ITERATION != -1 and DEV.UNSAFE):
        max_iteration = DEV.FORCED_MAX_ITERATION
    else:
        t = CONF["SAME_DIGIT_THRESHOLD"]
        n = CONF["NDIGITS"]
        max_iteration = int('9' * (t + 1) + '0' * abs(n - t)) // 10 + 1
    country_code = prefix_data.get_country_code()
    head_max_zeros = CONF["HEAD_MAX_ZEROS"]

    for cur_operator_code in prefix_data["OPERATOR_CODES"]:
        prefix = country_code + cur_operator_code
        computed_ndigits = ndigits - len(cur_operator_code)
        magnitude = 10 ** (computed_ndigits - 1)

        if (head_max_zeros == 0 and first_iteration < magnitude):
            first_iteration = magnitude

        for current_iteration in range(first_iteration, max_iteration):
            cur_phone_number_suffix = _append_heading_zeros(
                current_iteration, computed_ndigits, magnitude)

            if (not _reject_phone_number_suffix(cur_operator_code, cur_phone_number_suffix)):
                cur_phone_number = prefix + cur_phone_number_suffix
                db.save_phone_number(cur_phone_number, country_code,
                                  cur_operator_code, cur_phone_number_suffix)
                if (DEV.DEBUG_MODE):
                    DebugLogger("GENERATED_PHONE_NUMBER", cur_phone_number)


def _compute_first_iteration_value(metadatas: dict) -> int:
    if (DEV.UNSAFE):
        first_iteration = int(DEV.VERY_FIRST_ITERATION)
    else:
        first_iteration = 0
    if (metadatas is None):
        return first_iteration
    first_iteration = int(metadatas["phone_number_suffix"]) + 1
    return first_iteration


def _compute_operator_codes_slice(metadatas: Optional[dict], operator_codes: list):
    if (metadatas is None):
        return operator_codes
    last_operator_code = metadatas["phone_number_operator_code"]
    if last_operator_code in operator_codes:
        index = operator_codes.index(last_operator_code)
        operator_codes = operator_codes[index:]
    return operator_codes


def _skip_generation(data: Optional[dict]) -> bool:
    if (data is None):
        return False
    for key in data:
        if (data[key] != "-1"):
            return False
    return True


def _run_phone_numbers_generator() -> Void:
    prefix_data: PrefixData = CONF["PREFIX_DATA"]
    ndigits = CONF["NDIGITS"]
    reload_metas = db.retrieve_last_saved_phone_metadatas()
    op_codes = prefix_data.get_operator_codes_union()

    if (_skip_generation(reload_metas)):
        print(VOCAB["WARNING_MSG"]["ALREADY_REACHED_FINAL_EXIT_POINT"])
        return

    if (DEV.FORCED_FIRST_ITERATION != -1 and DEV.UNSAFE):
        first_iteration = DEV.FORCED_FIRST_ITERATION
    else:
        first_iteration = _compute_first_iteration_value(reload_metas)

    if (DEV.FORCED_OPERATOR_CODES and DEV.UNSAFE):
        prefix_data["OPERATOR_CODES"] = DEV.FORCED_OPERATOR_CODES
    else:
        prefix_data["OPERATOR_CODES"] = _compute_operator_codes_slice(reload_metas, op_codes)

    _do_generate(ndigits, prefix_data, first_iteration)
    db.append_finite_collection_indicator()
    print(VOCAB["SUCCESS_MSG"]["REACHED_FINAL_EXIT_POINT"])


def run() -> Void:
    config_validator.check_config(CONF)
    _run_phone_numbers_generator()

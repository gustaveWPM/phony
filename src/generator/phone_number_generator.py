# coding: utf-8

from generator.metaprog.logger import debug_logger as DebugLogger
from generator.metaprog.vocab import VOCAB
from generator.metaprog.aliases import Void
from generator.obj.contracts.prefix_data import PrefixData
import generator.config.rules.dev.generator as DEV
from generator.config.rules.generator import GENERATOR as CONF
import generator.config.builders.generator as builder
import generator.config.validator as config_validator
import generator.database.db as db
import generator.limits.phone_range_limit as Limit
from typing import Optional, List
import generator.smart_reload as SmartReload


def _reject_phone_number_suffix(op_code: str, phone_number_suffix: str) -> bool:
    head_max_zeros: int = CONF["HEAD_MAX_ZEROS"]
    same_digit_threshold: int = CONF["SAME_DIGIT_THRESHOLD"]
    same_consecutive_digit_threshold: int = CONF["CONSECUTIVE_SAME_DIGIT_THRESHOLD"]
    digits: str = "0123456789"
    whole_phone_number: str = op_code + phone_number_suffix
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


def _do_generate_range(r: range, block_len: int, magnitude: int, cur_op_code: str, country_code: str):
    prefix: str = country_code + cur_op_code

    for current_iteration in r:
        cur_phone_number_suffix: str = _append_heading_zeros(
            current_iteration, block_len, magnitude)
        if (not _reject_phone_number_suffix(cur_op_code, cur_phone_number_suffix)):
            cur_phone_number: str = prefix + cur_phone_number_suffix
            db.save_phone_number(cur_phone_number, country_code,
                                 cur_op_code, cur_phone_number_suffix)
            if (DEV.DEBUG_MODE):
                DebugLogger("GENERATED_PHONE_NUMBER", cur_phone_number)
"""             else:
                cur_phone_number: str = prefix + cur_phone_number_suffix
                print(f"Rejected: {cur_phone_number}")
"""


def _do_generate_loop(country_code: str, op_codes: List[str], metadatas: Optional[dict]):
    ndigits: int = CONF["NDIGITS"]

    for cur_op_code in op_codes:
        block_len: int = Limit.compute_range_len(cur_op_code)
        magnitude: int = 10 ** (block_len - 1)
        last_iteration: int = Limit.compute_range_end(ndigits, cur_op_code)
        first_iteration: int = Limit.compute_range_start(metadatas, cur_op_code, magnitude)

        if first_iteration == -1 or last_iteration == -1:
            break

        r = range(first_iteration, last_iteration)
        _do_generate_range(r, block_len, magnitude, cur_op_code, country_code)


def _do_generate(prefix_data: PrefixData, metadatas: dict) -> Void:
    country_code: str = prefix_data.country_code()
    op_codes_a: List[str] = []
    op_codes_b: List[str] = []

    if prefix_data.start_with_desk():
        op_codes_a = prefix_data.operator_desk_codes()
        op_codes_b = prefix_data.operator_mobile_codes()
    else:
        op_codes_a = prefix_data.operator_mobile_codes()
        op_codes_b = prefix_data.operator_desk_codes()

    _do_generate_loop(country_code, op_codes_a, metadatas)
    _do_generate_loop(country_code, op_codes_b, metadatas)


def _skip_generation(data: Optional[dict]) -> bool:
    if (data is None):
        return False
    return db.is_finite_collection(data)


def build_generator_config() -> Void:
    builder.append_dynamic_conf(CONF)


def _run_phone_numbers_generator() -> Void:
    prefix_data: PrefixData = CONF["PREFIX_DATA"]
    reload_metas: dict = db.retrieve_last_saved_phone_metadatas()

    if (_skip_generation(reload_metas)):
        print(VOCAB["WARNING_MSG"]["ALREADY_REACHED_FINAL_EXIT_POINT"])
        return

    if (DEV.FORCED_OPERATOR_CODES and DEV.UNSAFE):
        prefix_data.force_op_codes(DEV.FORCED_OPERATOR_CODES)
    else:
        SmartReload.slice_op_codes(reload_metas, prefix_data)

    _do_generate(prefix_data, reload_metas)
    db.append_finite_collection_indicator()
    print(VOCAB["SUCCESS_MSG"]["REACHED_FINAL_EXIT_POINT"])


def run() -> Void:
    build_generator_config()
    config_validator.check_config(CONF)
    _run_phone_numbers_generator()

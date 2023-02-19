# coding: utf-8

from generator.debug.logger import debug_logger as debug_logger
from generator.debug.vocab import VOCAB as DEBUG_VOCAB
from generator.metaprog.types import Void
from generator.obj.contracts.prefix_data import PrefixData
from generator.config.rules.generator import GENERATOR as GENERATOR_CONFIG
from generator.config.rules.dev.database import DB as DATABASE_CONFIG
import generator.config.rules.dev.debugger as DEBUGGER_CONFIG
import generator.config.rules.dev.generator as DEV_CONFIG
import generator.config.builders.generator as generator_config_builder
import generator.config.builders.database as database_config_builder
import generator.config.validator as config_validator
import generator.database.db as database
import generator.phone_range_limit as limit
import generator.smart_reload as smart_reload

from typing import Optional, List


def _is_banned_op_code(op_code: str) -> bool:
    banned_op_codes: List[str] = GENERATOR_CONFIG["BANNED_OPERATOR_CODES"]

    for cur_banned_op_code in banned_op_codes:
        if op_code == cur_banned_op_code:
            return True
    return False


def _reject_phone_number_suffix(op_code: str, phone_number_suffix: str) -> bool:
    last_block_head_max_zeros: int = GENERATOR_CONFIG["LAST_BLOCK_HEAD_MAX_ZEROS"]
    same_digit_threshold: int = GENERATOR_CONFIG["SAME_DIGIT_THRESHOLD"]
    same_consecutive_digit_threshold: int = GENERATOR_CONFIG["CONSECUTIVE_SAME_DIGIT_THRESHOLD"]
    digits: str = "0123456789"
    whole_phone_number: str = op_code + phone_number_suffix
    banned_pattern: str = ''
    banned_op_codes: List[str] = GENERATOR_CONFIG["BANNED_OPERATOR_CODES"]

    banned_pattern = '0' * (last_block_head_max_zeros + 1)
    if phone_number_suffix.startswith(banned_pattern):
        return True

    for banned_pattern in banned_op_codes:
        if banned_pattern == '':
            break
        if whole_phone_number.startswith(banned_pattern):
            return True

    for digit in digits:
        if whole_phone_number.count(digit) > same_digit_threshold:
            return True
        if same_consecutive_digit_threshold > 0:
            banned_pattern = digit * (same_consecutive_digit_threshold + 1)
            if banned_pattern in whole_phone_number:
                return True
    return False


def _append_heading_zeros(number: int, ndigits: int, magnitude: int) -> str:
    number_as_string: str = str(number)
    if number >= magnitude:
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
        if not _reject_phone_number_suffix(cur_op_code, cur_phone_number_suffix):
            cur_phone_number: str = prefix + cur_phone_number_suffix
            database.save_phone_number(cur_phone_number, country_code,
                                 cur_op_code, cur_phone_number_suffix)
            if DEV_CONFIG.DEBUG_MODE:
                debug_logger("GENERATED_PHONE_NUMBER", cur_phone_number)
        elif DEV_CONFIG.DEBUG_MODE and DEBUGGER_CONFIG.PRINT_REJECTED_PHONE_NUMBERS:
            cur_phone_number: str = prefix + cur_phone_number_suffix
            debug_logger("REJECTED_PHONE_NUMBER", cur_phone_number)



def _do_generate_loop(country_code: str, op_codes: List[str], metadatas: Optional[dict]):
    for cur_op_code in op_codes:
        if _is_banned_op_code(cur_op_code):
            if DEV_CONFIG.DEBUG_MODE and DEBUGGER_CONFIG.PRINT_REJECTED_OPERATOR_CODES:
                debug_logger("REJECTED_OPERATOR_CODE", cur_op_code)
            continue
        block_len: int = limit.compute_range_len(cur_op_code)
        magnitude: int = 10 ** (block_len - 1)
        last_iteration: int = limit.compute_range_end(cur_op_code)
        first_iteration: int = limit.compute_range_start(metadatas, cur_op_code, magnitude)
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
    if data is None:
        return False
    return database.is_finite_collection(data)


def build_config() -> Void:
    database_config_builder.append_dynamic_conf(DATABASE_CONFIG)
    generator_config_builder.append_dynamic_conf(GENERATOR_CONFIG)


def _run_phone_numbers_generator() -> Void:
    prefix_data: PrefixData = GENERATOR_CONFIG["PREFIX_DATA"]
    reload_metas: dict = database.retrieve_last_saved_phone_metadatas()

    if _skip_generation(reload_metas):
        print(DEBUG_VOCAB["WARNING_MSG"]["ALREADY_REACHED_FINAL_EXIT_POINT"])
        return

    if DEV_CONFIG.FORCED_OPERATOR_CODES and DEV_CONFIG.UNSAFE:
        prefix_data.force_op_codes(DEV_CONFIG.FORCED_OPERATOR_CODES)
    else:
        if not DEV_CONFIG.DISABLE_SMART_RELOAD:
            smart_reload.slice_op_codes(reload_metas, prefix_data)

    _do_generate(prefix_data, reload_metas)
    database.append_finite_collection_indicator()
    if DEV_CONFIG.DEBUG_MODE:
        print(DEBUG_VOCAB["SUCCESS_MSG"]["REACHED_FINAL_EXIT_POINT"])


def run() -> Void:
    build_config()
    config_validator.check_config(GENERATOR_CONFIG)
    _run_phone_numbers_generator()

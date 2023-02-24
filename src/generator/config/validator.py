# coding: utf-8


from generator.config.rules.generator import GENERATOR as GENERATOR_CONFIG
import generator.config.rules.dev.generator as DEV_CONFIG
from generator.sys.error import terminate, print_on_stderr
from generator.internal_lib.str import str_groupby
import generator.obj.implementations.countries as countries_service
from generator.obj.implementations.prefix_data import PrefixData
from generator.metaprog.types import Void


from typing import List


_MSG_PREFIX = "[CONFIGURATION ERROR]"
_STARTED_MSG = "Generation started..."


def _check_max_db_chunks_records_before_shuffle() -> Void:
    if DEV_CONFIG.DISABLE_SHUFFLE:
        return

    if DEV_CONFIG.MAX_DB_CHUNKS_RECORDS_BEFORE_SHUFFLE <= 0:
        terminate(f"{_MSG_PREFIX} 'MAX_DB_CHUNKS_RECORDS_BEFORE_SHUFFLE' should be greater than 0.")


def _check_db_entries_chunk_size() -> Void:
    if DEV_CONFIG.DB_ENTRIES_CHUNK_SIZE <= 0:
        terminate(f"{_MSG_PREFIX} 'DB_ENTRIES_CHUNK_SIZE' should be greater than 0.")


def __check_op_code_respects_same_digit_rule(config: dict, op_code: str) -> bool:
    groups: list = str_groupby(op_code)

    for same_consecutive_digit in [d[1] for d in groups]:
        if same_consecutive_digit > config["CONSECUTIVE_SAME_DIGIT_THRESHOLD"]:
            return False
    return True


def __do_check_op_codes(config: dict, op_codes: List[str]) -> bool:
    has_failed = False
    respect_same_digit_rule = True

    for cur_op_code in op_codes:
        ndigits: int = config["NDIGITS"]
        block_len: int = ndigits - len(cur_op_code)
        if block_len < 0:
            has_failed = True
            print_on_stderr(f"{_MSG_PREFIX} Found a bigger operator code than NDIGITS: {cur_op_code}")
        respect_same_digit_rule = __check_op_code_respects_same_digit_rule(config, cur_op_code)
        if not respect_same_digit_rule:
            has_failed = True
            print_on_stderr(f"{_MSG_PREFIX} Too much consecutive same digit in your op code: {cur_op_code}")
    return has_failed


def _check_op_codes(config: dict) -> Void:
    prefix_data: PrefixData = GENERATOR_CONFIG["PREFIX_DATA"]

    op_codes_a: List[str] = prefix_data.operator_desk_codes()
    op_codes_b: List[str] = prefix_data.operator_mobile_codes()

    make_crash = False
    has_failed = False

    has_failed = __do_check_op_codes(config, op_codes_a)
    if has_failed:
        make_crash = True

    has_failed = __do_check_op_codes(config, op_codes_b)
    if has_failed:
        make_crash = True

    if make_crash:
        terminate()


def _check_ndigit(config: dict) -> Void:
    if config["NDIGITS"] < config["SAME_DIGIT_THRESHOLD"]:
        terminate(f"{_MSG_PREFIX} Invalid configuration: NDIGITS should be greater than or equal to SAME_DIGIT_THRESHOLD.")
    if config["NDIGITS"] < config["LAST_BLOCK_HEAD_MAX_ZEROS"]:
        terminate(f"{_MSG_PREFIX} Invalid configuration: HEAD_MAX_ZEROS should be less than or equal to NDIGITS.")
    if config["NDIGITS"] <= 0:
        terminate(f"{_MSG_PREFIX} Invalid configuration: NDIGITS should be a positive value, greater than 0.")


def _check_same_digit_threshold(config: dict) -> Void:
    if config["SAME_DIGIT_THRESHOLD"] <= 0:
        terminate(f"{_MSG_PREFIX} Invalid configuration: SAME_DIGIT_THRESHOLD should be a positive value, greater than 0.")


def _check_head_max_zeros(config: dict) -> Void:
    if config["LAST_BLOCK_HEAD_MAX_ZEROS"] < 0:
        terminate(f"{_MSG_PREFIX} Invalid configuration: HEAD_MAX_ZEROS should be a positive value, less than or equal to NDIGITS.")


def _check_consecutive_same_digit_threshold(config: dict) -> Void:
    if config["CONSECUTIVE_SAME_DIGIT_THRESHOLD"] < 0:
        terminate(f"{_MSG_PREFIX} Invalid configuration: CONSECUTIVE_SAME_DIGIT_THRESHOLD should be a positive value, less than or equal to NDIGITS.")

    if config["CONSECUTIVE_SAME_DIGIT_THRESHOLD"] > config["SAME_DIGIT_THRESHOLD"]:
        terminate(f"{_MSG_PREFIX} Invalid configuration: CONSECUTIVE_SAME_DIGIT_THRESHOLD should be less than or equal to SAME_DIGIT_THRESHOLD.")


def on_build_check_target_options(options: dict) -> Void:
    start_with_desk: bool = GENERATOR_CONFIG["START_WITH_DESK_OPERATOR_CODES"]
    start_with_mobile: bool = GENERATOR_CONFIG["START_WITH_DESK_OPERATOR_CODES"] == False
    target_option_desk: bool = options["DESK"]
    target_option_mobile: bool = options["MOBILE"]

    if not target_option_desk and not target_option_mobile:
        terminate(f"{_MSG_PREFIX} Target options 'DESK' and 'MOBILE' are both setted to False.")

    if not target_option_desk and start_with_desk:
        terminate(f"{_MSG_PREFIX} Target option 'DESK' setted to False, but 'START_WITH_DESK_OPERATOR_CODES' setted to True.")

    if not target_option_mobile and start_with_mobile:
        terminate(f"{_MSG_PREFIX} Target option 'MOBILE' and 'START_WITH_DESK_OPERATOR_CODES' are both setted to False.")


def on_build_check_targeted_country(country: str) -> Void:
    if not countries_service.is_valid_country(country):
        terminate(f"{_MSG_PREFIX} Unknown country key value: {country}.")


def check_config(config: dict) -> Void:
    _check_max_db_chunks_records_before_shuffle()
    _check_db_entries_chunk_size()
    _check_ndigit(config)
    _check_same_digit_threshold(config)
    _check_head_max_zeros(config)
    _check_consecutive_same_digit_threshold(config)
    _check_op_codes(config)
    print(_STARTED_MSG)

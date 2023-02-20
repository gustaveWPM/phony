# coding: utf-8

from generator.metaprog.types import Void
import generator.obj.implementations.countries as countries_service
from generator.sys.error import terminate
from generator.obj.implementations.prefix_data import PrefixData
from generator.config.rules.generator import GENERATOR as GENERATOR_CONFIG
from generator.sys.error import print_on_stderr
from generator.internal_lib.str import str_groupby
from typing import List


_MSG_PREFIX = "[CONFIGURATION ERROR]"


def _check_op_code_respects_same_digit_rule(config: dict, op_code: str) -> bool:
    groups: dict = str_groupby(op_code)

    for same_consecutive_digit in [d[1] for d in groups]:
        if same_consecutive_digit > config["CONSECUTIVE_SAME_DIGIT_THRESHOLD"]:
            return False
    return True


def _do_check_op_codes(config: dict, op_codes: List[str]) -> bool:
    has_failed: bool = False
    respect_same_digit_rule: bool = True

    for cur_op_code in op_codes:
        ndigits: int = config["NDIGITS"]
        block_len: int = ndigits - len(cur_op_code)
        if block_len < 0:
            has_failed = True
            print_on_stderr(f"{_MSG_PREFIX} Found a bigger operator code than NDIGITS: {cur_op_code}")
        respect_same_digit_rule = _check_op_code_respects_same_digit_rule(config, cur_op_code)
        if not respect_same_digit_rule:
            has_failed = True
            print_on_stderr(f"{_MSG_PREFIX} Too much consecutive same digit in your op code: {cur_op_code}")
    return has_failed


def _check_op_codes(config: dict) -> Void:
    prefix_data: PrefixData = GENERATOR_CONFIG["PREFIX_DATA"]

    op_codes_a: List[str] = prefix_data.operator_desk_codes()
    op_codes_b: List[str] = prefix_data.operator_mobile_codes()

    make_crash: bool = False
    has_failed: bool = False

    has_failed = _do_check_op_codes(config, op_codes_a)
    if has_failed:
        make_crash = True

    has_failed = _do_check_op_codes(config, op_codes_b)
    if has_failed:
        make_crash = True

    if make_crash:
        terminate()


def _check_ndigit(config: dict) -> Void:
    if config["NDIGITS"] < config["SAME_DIGIT_THRESHOLD"]:
        terminate(f"{_MSG_PREFIX} Invalid configuration: NDIGITS should be greater than or equal to SAME_DIGIT_THRESHOLD")
    if config["NDIGITS"] < config["LAST_BLOCK_HEAD_MAX_ZEROS"]:
        terminate(f"{_MSG_PREFIX} Invalid configuration: HEAD_MAX_ZEROS should be less than or equal to NDIGITS")
    if config["NDIGITS"] <= 0:
        terminate(f"{_MSG_PREFIX} Invalid configuration: NDIGITS should be a positive value, greater than 0")


def _check_same_digit_threshold(config: dict) -> Void:
    if config["SAME_DIGIT_THRESHOLD"] <= 0:
        terminate(f"{_MSG_PREFIX} Invalid configuration: SAME_DIGIT_THRESHOLD should be a positive value, greater than 0")


def _check_head_max_zeros(config: dict) -> Void:
    if config["LAST_BLOCK_HEAD_MAX_ZEROS"] < 0:
        terminate(f"{_MSG_PREFIX} Invalid configuration: HEAD_MAX_ZEROS should be a positive value, less than or equal to NDIGITS")


def _check_consecutive_same_digit_threshold(config: dict) -> Void:
    if config["CONSECUTIVE_SAME_DIGIT_THRESHOLD"] < 0:
        terminate(f"{_MSG_PREFIX} Invalid configuration: CONSECUTIVE_SAME_DIGIT_THRESHOLD should be a positive value, less than or equal to NDIGITS")

    if config["CONSECUTIVE_SAME_DIGIT_THRESHOLD"] > config["SAME_DIGIT_THRESHOLD"]:
        terminate(f"{_MSG_PREFIX} Invalid configuration: CONSECUTIVE_SAME_DIGIT_THRESHOLD should be less than or equal to SAME_DIGIT_THRESHOLD")


def on_build_check_target_options(options: dict) -> Void:
    if not options["DESK"] and not options["MOBILE"]:
        terminate(f"{_MSG_PREFIX} Target options 'DESK' and 'MOBILE' are both setted to False.")


def on_build_check_targeted_country(country: str) -> Void:
    if not countries_service.is_valid_country(country):
        terminate(f"{_MSG_PREFIX} Unknown country key value: {country}.")


def check_config(config: dict) -> Void:
    _check_ndigit(config)
    _check_same_digit_threshold(config)
    _check_head_max_zeros(config)
    _check_consecutive_same_digit_threshold(config)
    _check_op_codes(config)

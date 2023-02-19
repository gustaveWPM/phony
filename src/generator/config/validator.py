# coding: utf-8

from generator.metaprog.types import Void
import generator.obj.services.countries as countries_service
from generator.sys.terminate import terminate


def _do_check_ndigit(config: dict) -> Void:
    if config["NDIGITS"] < config["SAME_DIGIT_THRESHOLD"]:
        terminate("Invalid configuration: NDIGITS should be greater than or equal to SAME_DIGIT_THRESHOLD")
    if config["NDIGITS"] < config["LAST_BLOCK_HEAD_MAX_ZEROS"]:
        terminate("Invalid configuration: HEAD_MAX_ZEROS should be less than or equal to NDIGITS")
    if config["NDIGITS"] <= 0:
        terminate("Invalid configuration: NDIGITS should be a positive value, greater than 0")


def _do_check_same_digit_threshold(config: dict) -> Void:
    if config["SAME_DIGIT_THRESHOLD"] <= 0:
        terminate("Invalid configuration: SAME_DIGIT_THRESHOLD should be a positive value, greater than 0")


def _do_check_head_max_zeros(config: dict) -> Void:
    if config["LAST_BLOCK_HEAD_MAX_ZEROS"] < 0:
        terminate("Invalid configuration: HEAD_MAX_ZEROS should be a positive value, less than or equal to NDIGITS")


def _do_check_consecutive_same_digit_threshold(config: dict) -> Void:
    if config["CONSECUTIVE_SAME_DIGIT_THRESHOLD"] < 0:
        terminate("Invalid configuration: CONSECUTIVE_SAME_DIGIT_THRESHOLD should be a positive value, less than or equal to NDIGITS")

    if config["CONSECUTIVE_SAME_DIGIT_THRESHOLD"] > config["SAME_DIGIT_THRESHOLD"]:
        terminate("Invalid configuration: CONSECUTIVE_SAME_DIGIT_THRESHOLD should be less than or equal to SAME_DIGIT_THRESHOLD")


def check_targeted_country(country: str) -> Void:
    if not countries_service.is_valid_country(country):
        terminate(f"Unknown country key value: {country}.")


def check_config(config: dict) -> Void:
    _do_check_ndigit(config)
    _do_check_same_digit_threshold(config)
    _do_check_head_max_zeros(config)
    _do_check_consecutive_same_digit_threshold(config)

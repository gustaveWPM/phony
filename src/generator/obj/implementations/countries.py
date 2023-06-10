# coding: utf-8


from typing import List


def is_valid_country(conf: dict) -> bool:
    return conf["TARGET"]["COUNTRY"] in conf["COUNTRIES"]


def get_country_mobile_operators_codes(conf: dict, targeted_country_key: str) -> List[str]:
    return conf["COUNTRIES"][targeted_country_key]["OPERATORS_CODES"]["MOBILE"]


def get_country_landline_operators_codes(conf: dict, targeted_country_key: str) -> List[str]:
    return conf["COUNTRIES"][targeted_country_key]["OPERATORS_CODES"]["LANDLINE"]


def get_country_code(conf: dict, targeted_country_key: str) -> str:
    return conf["COUNTRIES"][targeted_country_key]["COUNTRY_CODE"]

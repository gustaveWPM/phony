# coding: utf-8

from config.rules.countries import COUNTRIES
from typing import List

_COUNTRIES_LIST: List[str] = list(COUNTRIES.keys())


def is_valid_country(key: str) -> bool:
    return key in _COUNTRIES_LIST


def get_country_mobile_operator_codes(key: str) -> List[str]:
    return COUNTRIES[key]["OPERATOR_CODES"]["MOBILE"]


def get_country_desk_operator_codes(key: str) -> List[str]:
    return COUNTRIES[key]["OPERATOR_CODES"]["DESK"]


def get_country_code(key: str) -> str:
    return COUNTRIES[key]["COUNTRY_CODE"]

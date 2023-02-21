# coding: utf-8


from generator.config.rules.countries import COUNTRIES

from typing import List


_COUNTRIES_LIST: List[str] = list(COUNTRIES.keys())


def is_valid_country(targeted_country_key: str) -> bool:
    return targeted_country_key in _COUNTRIES_LIST


def get_country_mobile_operator_codes(targeted_country_key: str) -> List[str]:
    return COUNTRIES[targeted_country_key]["OPERATOR_CODES"]["MOBILE"]


def get_country_desk_operator_codes(targeted_country_key: str) -> List[str]:
    return COUNTRIES[targeted_country_key]["OPERATOR_CODES"]["DESK"]


def get_country_code(targeted_country_key: str) -> str:
    return COUNTRIES[targeted_country_key]["COUNTRY_CODE"]

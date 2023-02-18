# coding: utf-8

from metaprog.aliases import Void
from typing import List
import obj.services.countries as countries_service
from obj.contracts.prefix_data import PrefixData

def _do_generate_prefix_data(country: str, options: dict) -> PrefixData:
    if not options["DESK"] and not options["MOBILE"]:
        raise ValueError("Invalid configuration: 'DESK' and 'MOBILE' are both setted to False.")

    operator_desk_codes: List[str] = []
    operator_mobile_codes: List[str] = []

    country_code: str = countries_service.get_country_code(country)

    if options["DESK"]:
        operator_desk_codes = countries_service.get_country_desk_operator_codes(country)
    if options["MOBILE"]:
        operator_mobile_codes = countries_service.get_country_mobile_operator_codes(country)

    prefix_data: PrefixData = PrefixData(country_code, operator_desk_codes, operator_mobile_codes)
    return prefix_data


def _generate_prefix_data(target: dict) -> PrefixData:
    country: str = target["COUNTRY"]
    options: dict = target["OPTIONS"]

    if not countries_service.is_valid_country(country):
        raise ValueError(f"Unknown country key value: {country}.")

    return _do_generate_prefix_data(country, options)


def append_dynamic_conf(conf: dict) -> Void:
    target: dict = conf["TARGET"]
    conf["PREFIX_DATA"]: PrefixData = _generate_prefix_data(target)
    return conf

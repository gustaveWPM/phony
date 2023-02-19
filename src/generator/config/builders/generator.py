# coding: utf-8

from generator.metaprog.aliases import Void
from generator.config.validator import check_targeted_country
import generator.obj.services.countries as countries_service
from generator.obj.contracts.prefix_data import PrefixData
from generator.config.rules.countries import COUNTRIES
from typing import List


def _append_fine_tuning_attributes(conf: dict, target: dict) -> Void:
    country: str = target["COUNTRY"]
    fine_tuning_dict: dict = COUNTRIES[country]["FINE_TUNING"]

    for key in fine_tuning_dict:
        conf[key] = fine_tuning_dict[key]


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

    check_targeted_country(country)
    return _do_generate_prefix_data(country, options)


def _append_prefix_data(target: dict) -> PrefixData:
    prefix_data: PrefixData = _generate_prefix_data(target)
    return prefix_data


def append_dynamic_conf(conf: dict) -> Void:
    target: dict = conf["TARGET"]
    conf["PREFIX_DATA"] = _append_prefix_data(target)
    _append_fine_tuning_attributes(conf, target)

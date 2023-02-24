# coding: utf-8


from generator.config.rules.countries import COUNTRIES
from generator.config.validator import on_build_check_targeted_country, on_build_check_target_options
import generator.obj.implementations.countries as countries_service
from generator.obj.implementations.prefix_data import PrefixData
from generator.metaprog.types import Void


from typing import List


def _append_fine_tuning_attributes(conf: dict, target: dict) -> Void:
    key: str = target["COUNTRY"]
    fine_tuning: dict = COUNTRIES[key]["FINE_TUNING"]

    for key in fine_tuning:
        conf[key] = fine_tuning[key]


def _do_generate_prefix_data(country: str, options: dict) -> PrefixData:
    on_build_check_target_options(options)

    operator_desk_codes: List[str] = []
    operator_mobile_codes: List[str] = []

    country_code: str = countries_service.get_country_code(country)

    if options["DESK"]:
        operator_desk_codes = countries_service.get_country_desk_operator_codes(country)
    if options["MOBILE"]:
        operator_mobile_codes = countries_service.get_country_mobile_operator_codes(country)

    prefix_data = PrefixData(country_code, operator_desk_codes, operator_mobile_codes)
    return prefix_data


def _append_prefix_data(target: dict) -> PrefixData:
    country: str = target["COUNTRY"]
    options: dict = target["OPTIONS"]

    on_build_check_targeted_country(country)
    return _do_generate_prefix_data(country, options)


def append_dynamic_conf(conf: dict) -> Void:
    target: dict = conf["TARGET"]
    conf["PREFIX_DATA"] = _append_prefix_data(target)
    _append_fine_tuning_attributes(conf, target)

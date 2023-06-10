# coding: utf-8


from generator.config.validator import on_build_check_targeted_country, on_build_check_target_options
import generator.obj.implementations.countries as countries_service
from generator.obj.implementations.prefix_data import PrefixData
from generator.metaprog.types import Void
from generator.metaprog.runtime_imports import runtime_import
from generator.sys.error import terminate, print_on_stderr


from typing import List
import os


_MSG_PREFIX = "[CONFIGURATION ERROR]"

def _append_dynamic_countries_config(conf: dict) -> Void:
    def _get_artefacts_in_folder(folder: str) -> set:
        filenames = set()
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            if os.path.isfile(file_path):
                filenames.add(filename)
        return filenames

    artefacts_folder_root = "generator/config/rules/artefacts"
    artefacts_categories = ['country_code', 'fine_tuning', 'operators_codes']
    artefacts_folders = [f"{artefacts_folder_root}/{category}" for category in artefacts_categories]

    artefacts_folders_head = artefacts_folders[0]
    print(artefacts_folders_head)
    filenames = _get_artefacts_in_folder(artefacts_folders_head)

    rejected_folders = []
    for folder_path in artefacts_folders[1:]:
        if os.path.isdir(folder_path):
            current_artefact_folder_filenames = _get_artefacts_in_folder(folder_path)
            if current_artefact_folder_filenames != filenames:
                rejected_folders.append(folder_path)

            if rejected_folders:
                print_on_stderr(f"{_MSG_PREFIX} Expected this set of files in all the artefacts folders:", filenames)
                print_on_stderr(f"But those folders mismatch this rule:")
                for rejected_folder in rejected_folders:
                    print_on_stderr("- " + rejected_folder)
                terminate("\nInvalid artefacts: missing or foreign files!")

            countries = set()
            for filename in filenames:
                filename_without_extension = filename.replace(".py", "")
                countries.add(filename_without_extension)

            conf["COUNTRIES"] = {}
            for artefact_category in artefacts_categories:
                for country in countries:
                    artefact: str = artefact_category.upper()
                    key: str = country.upper()
                    module_path = artefacts_folder_root.replace("/", ".") + "." + artefact_category + "." + country
                    if key not in conf["COUNTRIES"]:
                        conf["COUNTRIES"][key] = {}
                    conf["COUNTRIES"][key][artefact] = runtime_import(module_path, artefact)


def _append_fine_tuning_attributes(conf: dict, target: dict) -> Void:
    key: str = target["COUNTRY"]
    fine_tuning: dict = conf['COUNTRIES'][key]["FINE_TUNING"]

    for key in fine_tuning:
        conf[key] = fine_tuning[key]


def _do_generate_prefix_data(conf: dict) -> PrefixData:
    country: str = conf["TARGET"]["COUNTRY"]
    options: dict = conf["TARGET"]["OPTIONS"]
    on_build_check_target_options(options)

    operator_landline_codes: List[str] = []
    operator_mobile_codes: List[str] = []

    country_code: str = countries_service.get_country_code(conf, country)

    if options["LANDLINE"]:
        operator_landline_codes = countries_service.get_country_landline_operators_codes(conf, country)
    if options["MOBILE"]:
        operator_mobile_codes = countries_service.get_country_mobile_operators_codes(conf, country)

    prefix_data = PrefixData(country_code, operator_landline_codes, operator_mobile_codes)
    return prefix_data


def _append_prefix_data(conf: dict) -> PrefixData:
    on_build_check_targeted_country(conf)
    return _do_generate_prefix_data(conf)


def append_dynamic_conf(conf: dict) -> Void:
    _append_dynamic_countries_config(conf)
    target: dict = conf["TARGET"]
    conf["PREFIX_DATA"] = _append_prefix_data(conf)
    _append_fine_tuning_attributes(conf, target)

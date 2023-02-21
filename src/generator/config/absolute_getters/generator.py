# coding: utf-8


from generator.config.rules.generator import GENERATOR
from generator.metaprog.runtime_imports import runtime_import
from generator.config.validator import on_build_check_targeted_country


_TARGETED_COUNTRY = GENERATOR["TARGET"]["COUNTRY"]
on_build_check_targeted_country(_TARGETED_COUNTRY)
_TARGET_SYMBOL = _TARGETED_COUNTRY.lower()
_FINE_TUNING_ARTEFACT_PATH = f"generator.config.rules.artefacts.fine_tuning.{_TARGET_SYMBOL}"
_FINE_TUNING = runtime_import(_FINE_TUNING_ARTEFACT_PATH, "FINE_TUNING")


def get_targeted_country() -> str:
    return _TARGETED_COUNTRY


def get_ndigits() -> int:
    return _FINE_TUNING["NDIGITS"]

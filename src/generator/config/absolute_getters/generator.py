# coding: utf-8


from generator.config.rules.generator import GENERATOR as GENERATOR_CONFIG
from generator.metaprog.runtime_imports import runtime_import


_TARGETED_COUNTRY = GENERATOR_CONFIG["TARGET"]["COUNTRY"]
_TARGET_SYMBOL = _TARGETED_COUNTRY.lower()
_FINE_TUNING_ARTEFACT_PATH = f"generator.config.rules.artefacts.fine_tuning.{_TARGET_SYMBOL}"
_FINE_TUNING = runtime_import(_FINE_TUNING_ARTEFACT_PATH, "FINE_TUNING")


def get_targeted_country() -> str:
    return _TARGETED_COUNTRY


def get_ndigits() -> int:
    return _FINE_TUNING["NDIGITS"]

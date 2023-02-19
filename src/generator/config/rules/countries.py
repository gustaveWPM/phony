# coding: utf-8

from generator.config.rules.artefacts.country_codes.france import COUNTRY_CODE as FR_CC
from generator.config.rules.artefacts.operator_codes.france import OPERATORS_CODES as FR_OC
from generator.config.rules.artefacts.fine_tuning.france import FINE_TUNING as FR_FT

COUNTRIES: dict = {
    "FRANCE": {
        "COUNTRY_CODE": FR_CC,
        "OPERATOR_CODES": FR_OC,
        "FINE_TUNING": FR_FT
    }
}

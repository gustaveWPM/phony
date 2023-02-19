# coding: utf-8

from config.rules.artefacts.country_codes.france import COUNTRY_CODE as FR_CC
from config.rules.artefacts.operator_codes.france import OPERATORS_CODES as FR_OC, FINE_TUNING as FR_FT

COUNTRIES: dict = {
    "FRANCE": {
        "COUNTRY_CODE": FR_CC,
        "OPERATOR_CODES": FR_OC,
        "FINE_TUNING": FR_FT
    }
}

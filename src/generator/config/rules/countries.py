# coding: utf-8


from generator.config.rules.artefacts.country_codes.france import COUNTRY_CODE as FR_CC
from generator.config.rules.artefacts.operator_codes.france import OPERATORS_CODES as FR_OC
from generator.config.rules.artefacts.fine_tuning.france import FINE_TUNING as FR_FT


from generator.config.rules.artefacts.country_codes.belgium import COUNTRY_CODE as BE_CC
from generator.config.rules.artefacts.operator_codes.belgium import OPERATORS_CODES as BE_OC
from generator.config.rules.artefacts.fine_tuning.belgium import FINE_TUNING as BE_FT


COUNTRIES = {
    "FRANCE": {
        "COUNTRY_CODE": FR_CC,
        "OPERATOR_CODES": FR_OC,
        "FINE_TUNING": FR_FT
    },

    "BELGIUM": {
        "COUNTRY_CODE": BE_CC,
        "OPERATOR_CODES": BE_OC,
        "FINE_TUNING": BE_FT
    }
}

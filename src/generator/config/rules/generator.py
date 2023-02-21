# coding: utf-8


from generator.metaprog.types import Schema


GENERATOR = Schema({
    "START_WITH_DESK_OPERATOR_CODES": False,
    "TARGET": {
        "COUNTRY": "FRANCE",
        "OPTIONS": {
            "DESK": False,
            "MOBILE": True
        }
    },

    "NDIGITS": "{BUILDER::ARTEFACT}",
    "SAME_DIGIT_THRESHOLD": "{BUILDER::ARTEFACT}",
    "CONSECUTIVE_SAME_DIGIT_THRESHOLD": "{BUILDER::ARTEFACT}",
    "LAST_BLOCK_HEAD_MAX_ZEROS": "{BUILDER::ARTEFACT}",
    "BANNED_OPERATOR_CODES": "{BUILDER::ARTEFACT}",
    "PREFIX_DATA": "{BUILDER::ARTEFACT}"
})

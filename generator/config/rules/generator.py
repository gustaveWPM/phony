# coding: utf-8

GENERATOR: dict = {
    "TARGET": {
        "COUNTRY": "FRANCE",
        "OPTIONS": {
            "DESK": False,
            "MOBILE": True
        }
    },

    "NDIGITS": "{BUILDER}",
    "SAME_DIGIT_THRESHOLD": "{BUILDER}",
    "CONSECUTIVE_SAME_DIGIT_THRESHOLD": "{BUILDER}",
    "HEAD_MAX_ZEROS": "{BUILDER}",
    "PREFIX_DATA": "{BUILDER}"
}


#================================================


def get_targeted_country() -> str:
    return GENERATOR["TARGET"]["COUNTRY"]


import config.builders.generator as builder
builder.append_dynamic_conf(GENERATOR)

# coding: utf-8

import config.builders.generator as builder

GENERATOR: dict = {
    # * ... Number of digits in the complete phone suffix, operator code included
    "NDIGITS": 9,
    # * ... Maximum same digit amount in the generated block
    "SAME_DIGIT_THRESHOLD": 5,
    # * ... Maximum consecutive same digit amount anywhere in the generated block
    "CONSECUTIVE_SAME_DIGIT_THRESHOLD": 5,
    # * ... Maximum consecutive 0 amount in the beginning of the generated block
    "HEAD_MAX_ZEROS": 1,

    "TARGET": {
        "COUNTRY": "FRANCE",
        "OPTIONS": {
            "DESK": False,
            "MOBILE": True
        }
    }
}

builder.append_dynamic_conf(GENERATOR)

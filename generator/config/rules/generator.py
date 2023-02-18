# coding: utf-8

import config.builders.generator as builder

GENERATOR: dict = {
    "TARGET": {
        "COUNTRY": "FRANCE",
        "OPTIONS": {
            "DESK": False,
            "MOBILE": True
        }
    }
}

builder.append_dynamic_conf(GENERATOR)

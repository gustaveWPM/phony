# coding: utf-8

GENERATOR: dict = {
    "TARGET": {
        "COUNTRY": "FRANCE",
        "OPTIONS": {
            "DESK": False,
            "MOBILE": True
        }
    }
}

# * ... I'll just inject all the rest of the config for you, you don't mind?

import config.builders.generator as builder
builder.append_dynamic_conf(GENERATOR)

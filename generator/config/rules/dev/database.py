# coding: utf-8

DB: dict = {
    "DISABLE_PERSISTENCE": False,
    "MONGO_DB_CONNECTION_URI": "mongodb://localhost:27017/",
    "MONGO_DB_NAME": "phonebook",

    "MONGO_DB_TABLE": "{BUILDER}"
}


#================================================


import config.builders.database as builder
builder.append_dynamic_conf(DB)

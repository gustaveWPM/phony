# coding: utf-8


from generator.metaprog.types import Schema


DB = Schema({
    "MONGO_DB_CONNECTION_URI": "mongodb://localhost:27017/",
    "MONGO_DB_NAME": "phonebook",

    "MONGO_DB_TABLE": "{BUILDER}"
})

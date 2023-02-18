GENERATOR_CONFIG = {
    "NDIGITS": 8, # * ... Number of digits in the pseudo randomly generated block
    "SAME_DIGIT_THRESHOLD": 4, # * ... Maximum same digit amount in the generated block
    "HEAD_MAX_ZEROS": 1, # * ... Maximum consecutive 0 amount in the beginning of the generated block

    "PREFIX_DATA": {
        "COUNTRY_CODE": "33",
        "OPERATOR_CODES": ["6", "7"]
    }
}

DB_CONFIG = {
    "MONGO_DB_CONNECTION_URI": "mongodb://localhost:27017/",
    "MONGO_DB_NAME": "phone_book",
    "MONGO_DB_TABLE": "france"
}

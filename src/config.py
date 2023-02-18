GENERATOR_CONFIG = {
    # * ... Number of digits in the complete phone suffix, operator code included
    "NDIGITS": 9,
    # * ... Maximum same digit amount in the generated block
    "SAME_DIGIT_THRESHOLD": 4,
    # * ... Maximum consecutive same digit amount anywhere in the generated block
    "CONSECUTIVE_SAME_DIGIT_THRESHOLD": 3,
    # * ... Maximum consecutive 0 amount in the beginning of the generated block
    "HEAD_MAX_ZEROS": 1,

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

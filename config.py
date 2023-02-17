GENERATOR_CONFIG = {
    "NDIGITS": 8, # * ... Number of digits in the pseudo randomly generated block
    "SAME_DIGIT_THRESHOLD": 4, # * ... Maximum same digit amount in the generated block
    "HEAD_MAX_ZEROS": 2, # * ... Maximum consecutive 0 amount in the beginning of the generated block

    "PREFIX_DATA": {
        "COUNTRY_CODE": "33",
        "OPERATOR_CODE": "6"
    }
}

DB_CONFIG = {
    "MONGO_DB_CONNECTION_ROUTE": "mongodb://localhost:27017/"
}

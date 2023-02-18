# coding: utf-8

COUNTRIES: dict = {
    "FRANCE": {
        "COUNTRY_CODE": "33",
        "OPERATOR_CODES": {
            "MOBILE": ["6", "7"],
            "DESK": ["1", "2", "3", "4", "5"]
        },
        "FINE_TUNING": {
            # * ... Number of digits in the complete phone suffix, operator code included
            "NDIGITS": 9,
            # * ... Maximum same digit amount in the generated block
            "SAME_DIGIT_THRESHOLD": 5,
            # * ... Maximum consecutive same digit amount anywhere in the generated block
            "CONSECUTIVE_SAME_DIGIT_THRESHOLD": 5,
            # * ... Maximum consecutive 0 amount in the beginning of the generated block
            "HEAD_MAX_ZEROS": 1,
        }
    }
}

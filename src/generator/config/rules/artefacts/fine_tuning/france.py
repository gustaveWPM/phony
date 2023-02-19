# coding: utf-8

FINE_TUNING: dict = {
    # * ... Number of digits in the complete phone suffix, operator code included
    "NDIGITS": 9,
    # * ... Maximum same digit amount in the generated pseudo-randomly block
    "SAME_DIGIT_THRESHOLD": 5,
    # * ... Maximum consecutive same digit amount anywhere in the pseudo-randomly generated block
    "CONSECUTIVE_SAME_DIGIT_THRESHOLD": 4,
    # * ... Maximum consecutive 0 amount in the beginning of the pseudo-randomly generated block
    "HEAD_MAX_ZEROS": 2,
    # * ... All phone numbers starting with those codes will be rejected. Set it to `{""}` to disable this feature.
    "BANNED_OPERATOR_CODES": {
        "60", "70", "10", "20", "30", "40", "50"
    }
}

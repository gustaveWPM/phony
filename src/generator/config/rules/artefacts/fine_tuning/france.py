# coding: utf-8

FINE_TUNING: dict = {
    # * ... Number of digits in the complete phone suffix, operator code included
    "NDIGITS": 9,
    # * ... Maximum same digit amount in the generated block
    "SAME_DIGIT_THRESHOLD": 5,
    # * ... Maximum consecutive same digit amount anywhere in the generated block
    "CONSECUTIVE_SAME_DIGIT_THRESHOLD": 4,
    # * ... Maximum consecutive 0 amount in the beginning of the generated block
    "HEAD_MAX_ZEROS": 1
}

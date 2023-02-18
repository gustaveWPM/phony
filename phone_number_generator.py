from config import GENERATOR_CONFIG as GEN_CONF
from db import *

DEBUG_MODE = False
FORCED_FIRST_ITERATION = -1

def reject_phone_number_suffix(phone_number_suffix: str) -> bool:
    head_max_zeros = GEN_CONF["HEAD_MAX_ZEROS"]
    same_digit_threshold = GEN_CONF["SAME_DIGIT_THRESHOLD"]
    digits = "0123456789"

    if (phone_number_suffix.startswith('0' * (head_max_zeros + 1))):
        return True
    for digit in digits:
        if (phone_number_suffix.count(digit) > same_digit_threshold):
            return True
    return False

def append_heading_zeros(number: int, ndigits: int, magnitude: int):
    number_as_string = str(number)
    if (number >= magnitude):
        return number_as_string
    number_len = len(number_as_string)
    number_of_zeros_to_append = abs(ndigits - number_len)
    phone_suffix = '0' * number_of_zeros_to_append + number_as_string
    return phone_suffix

def do_generate(ndigits: int, prefix_data: dict, first_iteration: int = 0):
    max_iteration = int('9' * (GEN_CONF["SAME_DIGIT_THRESHOLD"] + 1) + '0' * abs(GEN_CONF["NDIGITS"] - GEN_CONF["SAME_DIGIT_THRESHOLD"])) // 10 + 1 # * ... lol
    magnitude = 10 ** (ndigits - 1)
    country_code = prefix_data["COUNTRY_CODE"]
    head_max_zeros = GEN_CONF["HEAD_MAX_ZEROS"]

    if (head_max_zeros == 0 and first_iteration < magnitude):
        first_iteration = magnitude

    for current_operator_code in prefix_data["OPERATOR_CODES"]:
        prefix = country_code + current_operator_code

        for current_iteration in range(first_iteration, max_iteration):
            current_phone_number_suffix = append_heading_zeros(current_iteration, ndigits, magnitude)
            if (not reject_phone_number_suffix(current_phone_number_suffix)):
                currrent_phone_number = prefix + current_phone_number_suffix
                save_phone_number(currrent_phone_number, country_code, current_operator_code, current_phone_number_suffix)
                if (DEBUG_MODE):
                    print(f"[DEBUG] Generated phone number: {currrent_phone_number}")

def compute_first_iteration_value(metadatas):
    first_iteration = 0
    if (metadatas is None):
        return first_iteration
    first_iteration = int(metadatas["phone_number_suffix"]) + 1
    return first_iteration

def compute_operator_codes_slice(metadatas, operator_codes: list):
    if (metadatas is None):
        return operator_codes
    last_operator_code = metadatas["phone_number_operator_code"]
    index = operator_codes.index(last_operator_code)
    operator_codes = operator_codes[index:]
    return operator_codes

def config_error_handling():
    if (GEN_CONF["NDIGITS"] < GEN_CONF["SAME_DIGIT_THRESHOLD"]):
        raise ValueError("Invalid configuration: NDIGITS should be greater than or equal to SAME_DIGIT_THRESHOLD")
    if (GEN_CONF["NDIGITS"] < GEN_CONF["HEAD_MAX_ZEROS"]):
        raise ValueError("Invalid configuration: HEAD_MAX_ZEROS should be less than or equal to NDIGITS")
    if (GEN_CONF["SAME_DIGIT_THRESHOLD"] <= 0):
        raise ValueError("Invalid configuration: SAME_DIGIT_THRESHOLD should be a positive value, greater than 0")
    if (GEN_CONF["NDIGITS"] <= 0):
        raise ValueError("Invalid configuration: NDIGITS should be a positive value, greater than 0")
    if (GEN_CONF["HEAD_MAX_ZEROS"] < 0):
        raise ValueError("Invalid configuration: HEAD_MAX_ZEROS should be a positive value, less than or equal to NDIGITS")

def skip_generation(data) -> bool:
    if (data is None):
        return False
    for key in data:
        if (data[key] != "-1"):
            return False
    return True

def appendFiniteCollectionIndicator():
    save_phone_number("-1", "-1", "-1", "-1")

def run_phone_numbers_generator():
    config_error_handling()
    prefix_data = GEN_CONF["PREFIX_DATA"]
    ndigits = GEN_CONF["NDIGITS"]
    last_saved_phone_metadatas = retrieve_last_saved_phone_metadatas()
    if (skip_generation(last_saved_phone_metadatas)):
        print("You already have a finite phonebook.")
        return
    if (FORCED_FIRST_ITERATION == -1):
        first_iteration = compute_first_iteration_value(last_saved_phone_metadatas)
        prefix_data["OPERATOR_CODES"] = compute_operator_codes_slice(last_saved_phone_metadatas, prefix_data["OPERATOR_CODES"])
    else:
        first_iteration = FORCED_FIRST_ITERATION
    do_generate(ndigits, prefix_data, first_iteration)
    appendFiniteCollectionIndicator()
    print("Mission complete!")

if __name__ == "__main__":
    run_phone_numbers_generator()

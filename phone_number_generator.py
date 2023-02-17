import pymongo
from config import GENERATOR_CONFIG as GEN_CONF
from config import DB_CONFIG as DB_CONF

DEBUG_MODE = False

MONGO_CLIENT = pymongo.MongoClient(DB_CONF["MONGO_DB_CONNECTION_ROUTE"])
DB = MONGO_CLIENT["phone_book"]
DB_COL = DB["france"]

def retrieve_last_saved_phone_number_suffix() -> str:
    try:
        last_saved_phone_number_entry = DB_COL.find_one(sort=[( "_id", pymongo.DESCENDING )])
        last_saved_phone_number = last_saved_phone_number_entry["generated_suffix"]
        return last_saved_phone_number
    except:
        return '0'

def reject_phone_number_suffix(phone_number_suffix) -> bool:
    head_max_zeros = 2
    same_digit_threshold = GEN_CONF["SAME_DIGIT_THRESHOLD"]
    digits = "0123456789"

    if (phone_number_suffix.startswith('0' * head_max_zeros)):
        return True
    for digit in digits:
        if (phone_number_suffix.count(digit) > same_digit_threshold):
            return True
    return False

def save_phone_number(phone_number: str, prefix_data: dict, phone_number_suffix: str):
    country_code = prefix_data["COUNTRY_CODE"]
    operator_code = prefix_data["OPERATOR_CODE"]

    database_entry = {
        "phone_number": phone_number,
        "country_code": country_code,
        "operator_code": operator_code,
        "generated_suffix": phone_number_suffix
    }

    DB_COL.insert_one(database_entry)
    if (DEBUG_MODE):
        print(f"[DEBUG] Generated phone number: {phone_number}")

def append_heading_zeros(number, ndigits, magnitude):
    number_as_string = str(number)
    if (number >= magnitude):
        return number_as_string
    number_len = len(number_as_string)
    number_of_zeros_to_append = abs(ndigits - number_len)
    phone_suffix = '0' * number_of_zeros_to_append + number_as_string
    return phone_suffix

def do_generate(ndigits: int, prefix_data: dict, first_iteration: int = 0):
    max_iter = int('9' * (GEN_CONF["SAME_DIGIT_THRESHOLD"] + 1) + '0' * abs(GEN_CONF["NDIGITS"] - GEN_CONF["SAME_DIGIT_THRESHOLD"])) // 10 + 1 # * ... lol
    prefix = prefix_data["COUNTRY_CODE"] + prefix_data["OPERATOR_CODE"]
    magnitude = 10 ** (ndigits - 1)

    for i in range(first_iteration, max_iter):
        current_phone_number_suffix = append_heading_zeros(i, ndigits, magnitude)
        if (not reject_phone_number_suffix(current_phone_number_suffix)):
            currrent_phone_number = prefix + current_phone_number_suffix
            save_phone_number(currrent_phone_number, prefix_data, current_phone_number_suffix)

def config_error_handling():
    if (GEN_CONF["NDIGITS"] < GEN_CONF["SAME_DIGIT_THRESHOLD"]):
        raise ValueError("Invalid configuration: NDIGITS should be greater than or equal to SAME_DIGIT_THRESHOLD")
    if (GEN_CONF["SAME_DIGIT_THRESHOLD"] <= 0):
        raise ValueError("Invalid configuration: SAME_DIGIT_THRESHOLD should be a positive value, greater than 0")
    if (GEN_CONF["NDIGITS"] <= 0):
        raise ValueError("Invalid configuration: NDIGITS should be a positive value, greater than 0")

def run_phone_numbers_generator():
    config_error_handling()
    prefix_data = GEN_CONF["PREFIX_DATA"]
    ndigits = GEN_CONF["NDIGITS"]
    first_iteration = int(retrieve_last_saved_phone_number_suffix()) + 1
    do_generate(ndigits, prefix_data, first_iteration)
    print("Mission complete!")

if __name__ == "__main__":
    run_phone_numbers_generator()

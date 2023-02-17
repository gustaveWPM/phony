import pymongo

NDIGITS = 8 # * ... Number of digits in the pseudo randomly generated block
SAME_DIGIT_THRESHOLD = 4 # * ... Maximum same digit amount in the generated block
MONGO_DB_CONNECTION_ROUTE = "mongodb://localhost:27017/"

PREFIX_DATA = {
    "COUNTRY_CODE": "33",
    "OPERATOR_CODE": "6"
}

# * ... Don't edit this unless you know what you are doing
DEBUG_MODE = False
DIGITS = "0123456789"
MAGNITUDE = 10 ** (NDIGITS - 1)

MONGO_CLIENT = pymongo.MongoClient(MONGO_DB_CONNECTION_ROUTE)
DB = MONGO_CLIENT["phone_book"]
DB_COL = DB["hungary"]

def retrieve_last_saved_phone_number_suffix() -> str:
    try:
        last_saved_phone_number_entry = DB_COL.find_one(sort=[( '_id', pymongo.DESCENDING )])
        last_saved_phone_number = last_saved_phone_number_entry["generated_suffix"]
        return last_saved_phone_number
    except:
        return '0'

def reject_phone_number_suffix(phone_number_suffix) -> bool:
    head_max_zeros = 2
    same_digit_threshold = SAME_DIGIT_THRESHOLD

    if (phone_number_suffix.startswith('0' * head_max_zeros)):
        return True
    for digit in DIGITS:
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

def append_heading_zeros(number, ndigits):
    number_as_string = str(number)
    if (number >= MAGNITUDE):
        return number_as_string
    number_len = len(number_as_string)
    number_of_zeros_to_append = abs(ndigits - number_len)
    phone_suffix = '0' * number_of_zeros_to_append + number_as_string
    return phone_suffix

def do_generate(ndigits: int, prefix_data: dict, first_iteration: int = 0):
    max_iter = int('9' * (SAME_DIGIT_THRESHOLD + 1) + '0' * abs(NDIGITS - SAME_DIGIT_THRESHOLD)) // 10 + 1 # * ... lol
    prefix = prefix_data["COUNTRY_CODE"] + prefix_data["OPERATOR_CODE"]

    for i in range(first_iteration, max_iter):
        current_phone_number_suffix = append_heading_zeros(i, ndigits)
        if (not reject_phone_number_suffix(current_phone_number_suffix)):
            currrent_phone_number = prefix + current_phone_number_suffix
            save_phone_number(currrent_phone_number, prefix_data, current_phone_number_suffix)

def config_error_handling():
    if (NDIGITS < SAME_DIGIT_THRESHOLD):
        raise ValueError("Invalid configuration: NDIGITS should be greater than or equal to SAME_DIGIT_THRESHOLD")
    if (SAME_DIGIT_THRESHOLD <= 0):
        raise ValueError("Invalid configuration: SAME_DIGIT_THRESHOLD should be a positive value, greater than 0")
    if (NDIGITS <= 0):
        raise ValueError("Invalid configuration: NDIGITS should be a positive value, greater than 0")

def run_phone_numbers_generator():
    config_error_handling()
    prefix_data = PREFIX_DATA
    ndigits = NDIGITS
    first_iteration = int(retrieve_last_saved_phone_number_suffix()) + 1
    do_generate(ndigits, prefix_data, first_iteration)
    print("Mission complete!")

if __name__ == "__main__":
    run_phone_numbers_generator()

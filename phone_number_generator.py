DEBUG_MODE = True

PREFIX = "+336" # * ... Le prefixe du numéro de téléphone
NDIGITS = 8 # * ... Le nombre de numéros dans ton suffixe
SAME_DIGIT_THRESHOLD = 4 # * ... Le nombre maximum du même numéro dans le bloc généré

# * ... Don't edit this unless you know what you are doing
DIGITS = "0123456789"
MAGNITUDE = 10 ** (NDIGITS - 1)

def reject_phone_number_suffix(phone_number_suffix) -> bool:
    head_max_zeros = 2
    same_digit_threshold = SAME_DIGIT_THRESHOLD

    if (phone_number_suffix.startswith('0' * head_max_zeros)):
        return True
    for digit in DIGITS:
        if (phone_number_suffix.count(digit) > same_digit_threshold):
            return True
    return False

def save_phone_number(phone_number):
    if (DEBUG_MODE):
        print(f"[DEBUG] Generated phone number: {phone_number}")
    # * ... {ToDo} Sauvegarde phone_number

def append_heading_zeros(number, ndigits):
    number_as_string = str(number)
    if (number >= MAGNITUDE):
        return number_as_string
    number_len = len(number_as_string)
    number_of_zeros_to_append = abs(ndigits - number_len)
    phone_suffix = '0' * number_of_zeros_to_append + number_as_string
    return phone_suffix

def do_generate(ndigits: int, prefix: str, first_iteration: int = 0):
    max_iter = int('9' * (SAME_DIGIT_THRESHOLD + 1) + '0' * abs(NDIGITS - SAME_DIGIT_THRESHOLD)) // 10 + 1 # * ... lol
    for i in range(first_iteration, max_iter):
        current_phone_number_suffix = append_heading_zeros(i, ndigits)
        if (not reject_phone_number_suffix(current_phone_number_suffix)):
            currrent_phone_number = prefix + current_phone_number_suffix
            save_phone_number(currrent_phone_number)

def config_error_handling():
    if (NDIGITS < SAME_DIGIT_THRESHOLD):
        raise ValueError("Invalid configuration: NDIGITS should be greater than or equal to SAME_DIGIT_THRESHOLD")
    if (SAME_DIGIT_THRESHOLD <= 0):
        raise ValueError("Invalid configuration: SAME_DIGIT_THRESHOLD should be a positive value, greater than 0")
    if (NDIGITS <= 0):
        raise ValueError("Invalid configuration: NDIGITS should be a positive value, greater than 0")

def run_phone_numbers_generator():
    config_error_handling()
    prefix = PREFIX
    ndigits = NDIGITS
    do_generate(ndigits, prefix)
    print("Mission complete!")

if __name__ == "__main__":
    run_phone_numbers_generator()

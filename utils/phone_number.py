import re

def is_phone_valid(phone_number):
    EGYPT_PHONE_NUMBER_REGEX = r'^(\+?20)[1-9][0-9]{8}$'

    isValid = bool(re.search(EGYPT_PHONE_NUMBER_REGEX, phone_number))

    return isValid
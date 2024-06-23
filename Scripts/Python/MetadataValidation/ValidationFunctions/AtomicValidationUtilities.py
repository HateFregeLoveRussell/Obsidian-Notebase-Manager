from urllib.parse import urlparse
from datetime import datetime
from re import match
def validate_expected_value(value, desired_value):
    return True if value in desired_value else [f"Type Value Incorrect expected {desired_value}, got {value}"]

def validate_through_list(value, list):
    if value is None:
        return ["Field is Empty"]
    return True if value in list else [f"value must belong to {list}"]

def validate_url(value):
    try:
        result = urlparse(value)
        return True
    except ValueError:
        return ["URL value is not parseable"]

def basic_type_check(value, data_type):
    if value is None:
        return ["Value is Empty"]
    return True if isinstance(value, data_type) else [f"Value should be of type: {data_type}"]

def validate_ISBN(value):
    if not isinstance(value, str):
        return ["Expected string value"]

    # Remove hyphens and spaces
    isbn = value.replace('-', '').replace(' ', '')

    # Check if the length is correct (ISBN-10 has 10 digits, ISBN-13 has 13 digits)
    if len(isbn) not in (10, 13):
        return ["ISBN not correct length to be valid"]

    # Calculate the check digit based on ISBN length
    if len(isbn) == 10:
        check_digit = 0
        for i in range(9):
            check_digit += (i + 1) * int(isbn[i])
        check_digit %= 11
        check_digit = 'X' if check_digit == 10 else str(check_digit)
    else:  # ISBN-13
        check_digit = 0
        for i in range(0, 12, 2):
            check_digit += int(isbn[i])
            check_digit += int(isbn[i + 1]) * 3
        check_digit = (10 - (check_digit % 10)) % 10

    # Compare the calculated check digit with the last digit of ISBN
    return True if str(check_digit) == isbn[-1] else ["Not a Valid ISBN"]


def validate_datetime(value):
    value_type = type(value)
    if value_type is datetime.date:
        return True
    elif value_type is str:
        try:
            datetime.fromisoformat(value)
            return True
        except ValueError:
            return ["Date Field does not follow ISO 8601"]
    else:
        return ["Field Must be DateTime Type"]


def validate_alias_field(value):
    if value is None or value == "":
        return ["This field is Empty"]
    pattern = r'^[a-zA-Z0-9]+(?:-[a-zA-Z0-9]+)*$'
    return ["The chosen Alias is not a dash-seperated string of words"] if match(pattern, value) is None else True


def validate_list_of_type(value,typ):
    print('function called')
    if type(value) is typ:
        return True
    elif type(value) is list:
        for entry in value:
            if type(entry) is not typ:
                return [f"Entry {entry} in list not of type {typ}]"]
        return True

import re


def validate_decimal_value(value):
    if value is None or value < 0.:
        return False

    # Regular expression to match a decimal with 2 or less decimal places
    decimal_regex = re.compile(r'^\d+(\.\d{1,2})?$')

    # Check if the value matches the regex pattern
    if decimal_regex.match(str(value)):
        return True
    else:
        return False
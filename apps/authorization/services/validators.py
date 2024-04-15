from django.core.exceptions import ValidationError
import re


def only_int(value):
    if not value.isdigit():
        raise ValidationError("Code must contain only numbers")


def valid_identifier(value):
    pattern = r'\d{7}[A-Z]\d{3}[A-Z]{2}\d'
    match = re.fullmatch(pattern, value)
    if not match:
        raise ValidationError("Not valid passport identifier")

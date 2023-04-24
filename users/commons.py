from django.core.validators import validate_email
from django.core.exceptions import ValidationError

def valid_email(email):
    """
        Validates the given email address
    """
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False

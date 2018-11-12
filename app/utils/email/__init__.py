
from validate_email import validate_email

from app.utils.email.gmail import GMailAPIValidation

def MXDomainValidation(email):
    status = validate_email(email, check_mx=True)

    if status is not None and status == True:
        return True

    return False

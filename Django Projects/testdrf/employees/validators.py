from django.core.exceptions import ValidationError
from datetime import date


# Class based validators
class MinSalaryValidator:
    def __call__(self, value):
        if value < 30000:
            raise ValidationError("Salary must be at least ₹30,000.")


class HireDateValidator:
    def __call__(self, value):
        if value > date.today():
            raise ValidationError("Hire date cannot be in the future.")


# Function based validators
def validate_email(value):
    if value.split("@")[1] != "company.com":
        raise ValidationError(
            "[From validators.py] Invalid domain. Please ensure domain is @company.com."
        )

    return value


def validate_min_salary(value):
    if value < 30000:
        raise ValidationError("Salary must be at least ₹30,000.")

    return value


def validate_hire_date(value):
    if value > date.today():
        raise ValidationError("Hire date cannot be in the future.")

    return value

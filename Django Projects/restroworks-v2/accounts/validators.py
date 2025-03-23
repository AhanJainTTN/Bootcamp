import os
from django.core.exceptions import ValidationError


def validate_file_extension(file):
    """Only accepts .xls and .xlsx files."""

    if file:
        extension = os.path.splitext(file.name)[1]
        if extension not in {".xlsx", ".xls"}:
            raise ValidationError("Invalid file format. Please upload an Excel file.")

    return file

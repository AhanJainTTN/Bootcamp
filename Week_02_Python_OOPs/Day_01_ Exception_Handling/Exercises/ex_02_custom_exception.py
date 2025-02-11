"""
How to define a custom exception? What are the occasions we should define a custom exception? Explain with code.
"""

from typing import Optional


class InvalidPANError(Exception):
    """
    Raises an exception if the entered PAN details are not valid.

    Attributes:
        pan_details: input PAN which caused the error
        message: explanation of the error
    """

    def __init__(
        self,
        pan_details: str,
        message: Optional[str] = "Invalid PAN. Please check the entered details.",
    ):
        self.pan_details = pan_details
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        return f"{self.message} Entered PAN: {self.pan_details}."


"""
Here, we have overridden the constructor of the Exception class to accept our own custom arguments pan_details and message.
"""

try:
    pan_details = "ABCDE1234"

    if len(pan_details) != 10:
        raise InvalidPANError(
            pan_details, message="Invalid PAN length. Please check the entered details."
        )
except InvalidPANError as e:
    print(f"Error: {e}")

from django.core.exceptions import ValidationError
from PIL import Image


def validate_image(image):
    """Only accepts square images."""
    image = Image.open(image)
    width, height = image.size

    if width != height:
        raise ValidationError("Uploaded image must be a square.")

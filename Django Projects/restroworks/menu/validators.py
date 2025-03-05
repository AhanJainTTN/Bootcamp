from django.core.exceptions import ValidationError
from PIL import Image


# TODO: Try resizing images with PIL
def validate_image(image):
    """Only accepts square images."""

    if image:
        image = Image.open(image)
        width, height = image.size

        if width != height:
            raise ValidationError("Uploaded image must be a square.")

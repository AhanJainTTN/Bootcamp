from django.db import models
from menu.validators import validate_image


class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    image = models.ImageField(
        upload_to="menu/menu_items/",
        validators=[validate_image],
        help_text="Please upload an image with equal height and width.",
        null=True,
        blank=True,
        default="menu/default.png",
    )
    rating = models.FloatField(default=0.0, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # to track item changes

    def __str__(self):
        return f"{self.name}"

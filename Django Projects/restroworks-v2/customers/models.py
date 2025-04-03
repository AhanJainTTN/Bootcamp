from django.contrib.auth.models import User
from django.db import models
from django.core.validators import RegexValidator


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Links to auth_user
    email = models.EmailField(unique=True)
    phone = models.IntegerField(
        unique=True,
        validators=[
            RegexValidator(
                regex=r"^\d{10}$",
                message="Enter a valid 10 digit phone number without country code",
                code="invalid_phone_number",
            )
        ],
    )

    def __str__(self):
        return f"{self.user.username} {self.phone}"

from django.contrib.auth.models import User
from django.db import models


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Links to auth_user
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return f"{self.user.username}"

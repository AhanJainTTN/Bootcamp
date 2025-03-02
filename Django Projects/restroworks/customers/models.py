from django.contrib.auth.models import User
from django.db import models

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Links to auth_user
    phone = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

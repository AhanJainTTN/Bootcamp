from django import forms
from django.contrib.auth.models import User
from .models import Customer
from django.db import IntegrityError, transaction


class CustomerForm(forms.ModelForm):
    phone = forms.CharField(
        max_length=10,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "input-field", "placeholder": "Enter phone"}
        ),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "input-field", "placeholder": "Enter password"}
        ),
        required=True,
    )

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password"]
        widgets = {
            "username": forms.TextInput(
                attrs={"class": "input-field", "placeholder": "Enter username"}
            ),
            "first_name": forms.TextInput(
                attrs={"class": "input-field", "placeholder": "Enter first name"}
            ),
            "last_name": forms.TextInput(
                attrs={"class": "input-field", "placeholder": "Enter last name"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "input-field", "placeholder": "Enter email"}
            ),
        }

    # Django's User model requires passwords to be hashed before saving.
    # Using fields = ["password"] will create a normal text field, which is insecure.
    #  We also need password to be rendered as hidden field so we explicitly define it as a password field instead of just appending it to fields and hashing it using save.
    def save(self):
        # If commit=False is used, Django creates an instance of the model but does NOT save it to the database
        # commit=False because still need to hash password and link User to Customer
        # super().save(commit=False)creates a User instance but does not save it.
        try:
            with transaction.atomic():
                user = super().save(commit=False)
                user.set_password(self.cleaned_data["password"])
                user.save()
                user = Customer.objects.create(
                    user=user, phone=self.cleaned_data["phone"]
                )

            return user
        except IntegrityError:
            self.add_error("phone", "This phone number is already in use.")

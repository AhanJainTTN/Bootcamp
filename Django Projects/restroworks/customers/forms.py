from django import forms
from django.contrib.auth.models import User
from .models import Customer
from django.db import IntegrityError, transaction
from django.contrib.auth.forms import UserCreationForm


# Only username, password1 and password2 fields are available by default
# no need to explicitly hash passwords - already taken care of
class CustomerForm(UserCreationForm):
    phone = forms.CharField(
        max_length=10,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "input-field", "placeholder": "Enter phone"}
        ),
    )

    # TODO: Check why password1 and password2 work here and why not including username causes an error
    # TODO: Check order/flow of execution using Meta classes
    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            # "password1",
            # "password2",
        ]

        widgets = {
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {"class": "input-field", "placeholder": "Enter username"}
        )
        self.fields["password1"].widget.attrs.update(
            {"class": "input-field", "placeholder": "Enter password"}
        )
        self.fields["password2"].widget.attrs.update(
            {"class": "input-field", "placeholder": "Enter password"}
        )

    def save(self):
        try:
            with transaction.atomic():
                user = super().save()
                print(self.cleaned_data["email"])
                customer = Customer.objects.create(
                    user=user,
                    email=self.cleaned_data["email"],
                    phone=self.cleaned_data["phone"],
                )
            return customer
        # UNIQUE constraint failed: customers_customer.email
        # TODO: Find a better way. How much validation? HTML -> Forms -> Models. Which is the best way?
        except IntegrityError as e:
            print(str(e.__cause__))
            cause = str(e.__cause__).split(".")[1]
            self.add_error(f"{cause}", "Already in use. Please enter a unique value.")


# class CustomerForm(forms.ModelForm):
#     phone = forms.CharField(
#         max_length=10,
#         required=True,
#         widget=forms.TextInput(
#             attrs={"class": "input-field", "placeholder": "Enter phone"}
#         ),
#     )

#     class Meta:
#         model = User
#         fields = ["username", "first_name", "last_name", "email", "password"]
# widgets = {
#     "username": forms.TextInput(
#         attrs={"class": "input-field", "placeholder": "Enter username"}
#     ),
#     "password": forms.PasswordInput(
#         attrs={"class": "input-field", "placeholder": "Enter email"}
#     ),
#     "first_name": forms.TextInput(
#         attrs={"class": "input-field", "placeholder": "Enter first name"}
#     ),
#     "last_name": forms.TextInput(
#         attrs={"class": "input-field", "placeholder": "Enter last name"}
#     ),
#     "email": forms.EmailInput(
#         attrs={"class": "input-field", "placeholder": "Enter email"}
#     ),
# }

#     # Django's User model requires passwords to be hashed before saving.
#     # Using fields = ["password"] without using PasswordField/PasswordInput will create a normal text field, which is insecure. Even if we just set password attributes, we still need to hash it.
#     #  We also need password to be rendered as hidden field so we explicitly define it as a password field instead of just appending it to fields and hashing it using save.
# def save(self):
#     # If commit=False is used, Django creates an instance of the model but does NOT save it to the database
#     # commit=False because still need to hash password and link User to Customer
#     # super().save(commit=False)creates a User instance but does not save it.
#     try:
#         with transaction.atomic():
#             user = super().save(commit=False)
#             user.set_password(self.cleaned_data["password"])
#             user.save()
#             user = Customer.objects.create(
#                 user=user, phone=self.cleaned_data["phone"]
#             )

#         return user
#     except IntegrityError:
#         self.add_error("phone", "This phone number is already in use.")

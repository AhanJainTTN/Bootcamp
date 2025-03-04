from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User


class CustomerAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {"class": "input-field", "placeholder": "Enter username"}
        )
        self.fields["password"].widget.attrs.update(
            {"class": "input-field", "placeholder": "Enter password"}
        )

    # username
    # password = forms.CharField(
    #     widget=forms.PasswordInput(
    #         attrs={"class": "input-field", "placeholder": "Enter password"}
    #     ),
    #     required=True,
    # )

    # class Meta:
    #     model = User
    #     fields = ["username", "password"]
    #     widgets = {
    #         "username": forms.TextInput(
    #             attrs={"class": "input-field", "placeholder": "Enter username"}
    #         ),
    #         "password": forms.PasswordInput(
    #             attrs={"class": "input-field", "placeholder": "Enter email"}
    #         ),
    #     }

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from customers.models import Customer
from django.db import IntegrityError, transaction
from .validators import validate_file_extension

# TODO: Is it better to use a clean_field function on a unique field to check for uniqueness using Objects.filter() in addition to having a UNIQUE constraint at the database level or let the database check it and handle the IntegrityError exception it raises. If the database is going to check it regardless, is that not better for performance? If yes, does this mean in this context we use clean_field() mainly for convenience?

# Answer (Partial): Best to do both - clean_field makes it easier to send error messages to the user but is not entirely foolproof as there is a possibility that in the duration the query is being run, an entry with that email is inserted into the database. This will pass the uniqueness check but cause data inconsistency in the database. Part of the point of database-level constraints is to be atomic – to check the constraint and perform the insert at the same time, so no-one else can interfere in the middle.


# Only username, password1 and password2 fields are inherited - even though BaseUserCreation form's Meta class uses User model, it only defines fields = ("username", ) so username is inherited. Additionally, it also defines password1 and password2 explicitly so in total 3 fields are inherited.
# ModelForm is a regular Form which can automatically generate certain fields. The fields that are automatically generated depend on the content of the Meta class and, on which fields have already been defined declaratively. Basically, ModelForm will only generate fields that are missing from the form, or in other words, fields that weren’t defined declaratively.
# no need to explicitly hash passwords - already taken care of
class CustomerForm(UserCreationForm):
    phone = forms.CharField(
        max_length=10,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "input-field", "placeholder": "Enter phone"}
        ),
    )

    # TODO: Check order/flow of execution using Meta classes
    # fields or exclude must always be defined if using a meta class
    # fields from fields = [...] and explicilty defined fields are displayed
    # exclude takes precedence over fields
    # here excluding password1 and password2 has no effect as the inherited and explicity declared fields   override their inclusion or exclusion in the Meta class. Excluding username raises a KeyError exception because we are accessing that field in __init__. username exists in User so it's existence is controlled by the fields attribute of the meta class.
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
        # exclude only has control over the User fields - not the inherited or explicitly declared fields
        # https://code.djangoproject.com/ticket/8620#no2
        exclude = ["phone", "password1", "password2"]  # no effect

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

    # better way to add attributes as it does not override original InputFieldType
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

    # def clean_email(self):
    #     email = self.cleaned_data["email"]
    #     if User.objects.filter(email=email).exists():
    #         raise ValidationError(message="Email Already In Use.")

    #     return email

    def save(self):
        try:
            with transaction.atomic():
                user = super().save()
                customer = Customer.objects.create(
                    user=user,
                    email=self.cleaned_data["email"],
                    phone=self.cleaned_data["phone"],
                )
            return customer
        # TODO: Find a better way. How much validation? HTML -> Forms -> Models. Which is the best practice?
        except IntegrityError as e:
            # print(str(e.__cause__))
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


class ExcelForm(forms.Form):
    excel_file = forms.FileField(
        required=True, allow_empty_file=False, validators=[validate_file_extension]
    )

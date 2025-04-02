from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from customers.models import Customer
from django.db import IntegrityError, transaction
from .validators import validate_file_extension

# TODO: Is it better to use a clean_field function on a unique field to check for uniqueness using Objects.filter() in addition to having a UNIQUE constraint at the database level or let the database check it and handle the IntegrityError exception it raises. If the database is going to check it regardless, is that not better for performance? If yes, does this mean in this context we use clean_field() mainly for convenience?

# Answer (Partial): Best to do both - clean_field makes it easier to send error messages to the user but is not entirely foolproof as there is a possibility that in the duration the query is being run, an entry with that email is inserted into the database. This will pass the uniqueness check but cause data inconsistency in the database. Part of the point of database-level constraints is to be atomic – to check the constraint and perform the insert at the same time, so no-one else can interfere in the middle. Checking before the DB does is benefitial for checks which fail since we avoid DB hit for each fail.


# Only password1 and password2 fields are inherited - even though BaseUserCreation form's Meta class uses User model, it only defines fields = ("username", ) inside the Meta class so username is not inherited. It only defines password1 and password2 explicitly so in total 2 fields are inherited. This is why excluding username but keeping it in __init__()
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

    # Meta class has no control over non model fields - need to be styled in __init__()
    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
        ]

    # better way to add attributes as it does not override original InputFieldType
    # field must be present in Meta class fields or inherited or defined explicitly
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {"class": "input-field", "placeholder": "Enter username"}
        )
        self.fields["first_name"].widget.attrs.update(
            {"class": "input-field", "placeholder": "Enter username"}
        )
        self.fields["last_name"].widget.attrs.update(
            {"class": "input-field", "placeholder": "Enter username"}
        )
        self.fields["email"].widget.attrs.update(
            {"class": "input-field", "placeholder": "Enter username"}
        )

        # inherited fields
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
                customer = Customer.objects.create(
                    user=user,
                    email=self.cleaned_data["email"],
                    phone=self.cleaned_data["phone"],
                )
            return customer
        # TODO: Find a better way. How much validation? HTML -> Forms -> Models. Which is the best practice?
        except IntegrityError as e:
            cause = str(e.__cause__).split(".")[1]
            self.add_error(f"{cause}", "Already in use. Please enter a unique value.")


class CustomerAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {"class": "input-field", "placeholder": "Enter username"}
        )
        self.fields["password"].widget.attrs.update(
            {"class": "input-field", "placeholder": "Enter password"}
        )


class ExcelForm(forms.Form):
    excel_file = forms.FileField(
        required=True, allow_empty_file=False, validators=[validate_file_extension]
    )

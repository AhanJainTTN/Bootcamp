from rest_framework import serializers
from .models import Employees
from .validators import (
    MinSalaryValidator,
    HireDateValidator,
    validate_email,
    validate_min_salary,
    validate_hire_date,
)


class EmployeeSerializer(serializers.ModelSerializer):
    # salary = serializers.IntegerField(validators=[MinSalaryValidator()])
    # hire_date = serializers.DateField(validators=[HireDateValidator()])
    # email = serializers.EmailField(validators=[validate_email])
    salary = serializers.IntegerField(validators=[validate_min_salary])
    hire_date = serializers.DateField(validators=[validate_hire_date])

    class Meta:
        model = Employees
        fields = "__all__"

    def validate_email(self, email):
        if email.split("@")[1] != "company.com":
            raise serializers.ValidationError(
                "[From EmployeeSerialiser validate_email()] Invalid domain. Please ensure domain is @company.com."
            )

        return email

    def validate(self, data):
        # if data.get("email").split("@")[1] != "company.com":
        #     raise serializers.ValidationError(
        #         "[From EmployeeSerialiser validate()] Invalid domain. Please ensure domain is @company.com."
        #     )

        if (
            data.get("manager_id")
            and not Employees.objects.filter(employee_id=data["manager_id"]).exists()
        ):
            raise serializers.ValidationError(
                "Invalid manager ID. The manager must exist in the database."
            )

        return data


# https://www.django-rest-framework.org/api-guide/validators/
# Validation in Django REST framework serializers is handled a little differently to how validation works in Django's ModelForm class. With ModelForm the validation is performed partially on the form, and partially on the model instance. With REST framework the validation is performed entirely on the serializer class.

# Order of validation -> validators.py (validators=[] for all fields, automatically generated if using ModelSerializer) -> validate_field() -> validate()

# >>> from employees.serializers import EmployeeSerializer
# >>> obj = EmployeeSerializer()
# >>> print(repr(obj))
# EmployeeSerializer():
#     employee_id = IntegerField(read_only=True)
#     email = EmailField(validators=[<function validate_email>])
#     first_name = CharField(max_length=512)
#     last_name = CharField(allow_blank=True, allow_null=True, max_length=512, required=False)
#     phone_number = CharField(max_length=12, validators=[<django.core.validators.RegexValidator object>, <UniqueValidator(queryset=Employees.objects.all())>])
#     hire_date = DateField()
#     job_id = CharField(max_length=512)
#     salary = IntegerField(max_value=2147483647, min_value=-2147483648)
#     manager_id = IntegerField(allow_null=True, max_value=2147483647, min_value=-2147483648, required=False)

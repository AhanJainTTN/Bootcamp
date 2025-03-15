from rest_framework import serializers
from .models import Employees


# https://www.django-rest-framework.org/api-guide/validators/
# Validation in Django REST framework serializers is handled a little differently to how validation works in Django's ModelForm class. With ModelForm the validation is performed partially on the form, and partially on the model instance. With REST framework the validation is performed entirely on the serializer class.
class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employees
        fields = "__all__"

    def validate_email(self, email):
        if email.split("@") != "company.com":
            raise serializers.ValidationError(
                "Invalid domain. Please ensure domain is @company.com."
            )

        return email

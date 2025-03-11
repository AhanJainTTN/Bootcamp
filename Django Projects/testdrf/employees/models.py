# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.core.validators import RegexValidator


class Employees(models.Model):
    employee_id = models.AutoField(
        primary_key=True, db_column="EMPLOYEE_ID"
    )  # Field name made lowercase.
    first_name = models.CharField(
        db_column="FIRST_NAME", max_length=512
    )  # Field name made lowercase.
    last_name = models.CharField(
        db_column="LAST_NAME", max_length=512, blank=True, null=True
    )  # Field name made lowercase.
    email = models.EmailField(
        db_column="EMAIL", max_length=512, unique=True
    )  # Field name made lowercase.
    phone_number = models.CharField(
        db_column="PHONE_NUMBER",
        max_length=12,
        unique=True,
        validators=[
            RegexValidator(
                regex=r"^(\d{3}.){2}\d{4}$",
                message="Enter a valid phone number in the format XXX.XXX.XXXX",
                code="invalid_phone_number",
            )
        ],
    )  # Field name made lowercase.
    hire_date = models.DateField(db_column="HIRE_DATE")  # Field name made lowercase.
    job_id = models.CharField(
        db_column="JOB_ID", max_length=512
    )  # Field name made lowercase.
    salary = models.IntegerField(db_column="SALARY")  # Field name made lowercase.
    manager_id = models.IntegerField(
        db_column="MANAGER_ID", blank=True, null=True
    )  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = "employees"
        verbose_name_plural = "Employees"

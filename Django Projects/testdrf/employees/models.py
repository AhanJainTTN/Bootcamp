from django.db import models


class Employees(models.Model):
    employee_id = models.BigAutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(unique=True, max_length=256)
    phone = models.CharField(unique=True, max_length=10)
    hire_date = models.DateField()
    salary = models.IntegerField(blank=True, null=True)
    job = models.ForeignKey("Jobs", models.CASCADE, blank=True, null=True)
    manager = models.ForeignKey("self", models.CASCADE, blank=True, null=True)

    class Meta:
        managed = True
        db_table = "employees"
        verbose_name_plural = "Employees"

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.employee_id})"


class Jobs(models.Model):
    job_id = models.BigAutoField(primary_key=True)
    job_code = models.CharField(unique=True, max_length=50)
    job_title = models.CharField(unique=True, max_length=50)

    class Meta:
        managed = True
        db_table = "jobs"
        verbose_name_plural = "Jobs"

    def __str__(self):
        return f"{self.job_code}"

# Generated by Django 5.1.7 on 2025-03-26 07:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Jobs',
            fields=[
                ('job_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('job_code', models.CharField(max_length=50, unique=True)),
                ('job_title', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Jobs',
                'db_table': 'jobs',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Employees',
            fields=[
                ('employee_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(blank=True, max_length=50, null=True)),
                ('email', models.EmailField(max_length=256, unique=True)),
                ('phone', models.CharField(max_length=10, unique=True)),
                ('hire_date', models.DateField()),
                ('salary', models.IntegerField(blank=True, null=True)),
                ('manager', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='employees.employees')),
                ('job', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='employees.jobs')),
            ],
            options={
                'verbose_name_plural': 'Employees',
                'db_table': 'employees',
                'managed': True,
            },
        ),
    ]

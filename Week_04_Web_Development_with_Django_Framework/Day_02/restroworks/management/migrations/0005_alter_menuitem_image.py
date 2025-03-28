# Generated by Django 5.1.6 on 2025-02-25 11:12

import management.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0004_alter_menuitem_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuitem',
            name='image',
            field=models.ImageField(help_text='Please upload an image with equal height and width.', null=True, upload_to='menu_items/', validators=[management.models.validate_image]),
        ),
    ]

# Generated by Django 5.1.6 on 2025-02-27 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0006_alter_menuitem_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuitem',
            name='rating',
            field=models.FloatField(blank=True, null=True),
        ),
    ]

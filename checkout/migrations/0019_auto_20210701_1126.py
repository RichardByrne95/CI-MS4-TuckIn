# Generated by Django 3.1.7 on 2021-07-01 10:26

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0018_auto_20210701_1059'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='phone_number',
            field=models.CharField(default='', max_length=15, validators=[django.core.validators.MinLengthValidator(limit_value=7)]),
        ),
    ]

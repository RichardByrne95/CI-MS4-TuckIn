# Generated by Django 3.1.7 on 2021-07-01 09:59

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0017_auto_20210518_1559'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='phone_number',
            field=models.CharField(default='', max_length=20, validators=[django.core.validators.MinLengthValidator(limit_value=7)]),
        ),
    ]
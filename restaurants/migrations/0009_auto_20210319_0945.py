# Generated by Django 3.1.7 on 2021-03-19 09:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0008_auto_20210318_1559'),
    ]

    operations = [
        migrations.RenameField(
            model_name='restaurant',
            old_name='delivery_charge',
            new_name='delivery_cost',
        ),
    ]

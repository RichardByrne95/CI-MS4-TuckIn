# Generated by Django 3.1.7 on 2021-05-14 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0015_orderlineitem_additional_details'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='original_bag',
            field=models.JSONField(default=dict),
        ),
    ]

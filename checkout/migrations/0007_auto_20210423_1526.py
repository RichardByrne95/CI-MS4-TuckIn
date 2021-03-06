# Generated by Django 3.1.7 on 2021-04-23 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0006_auto_20210423_1455'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='address_1',
            field=models.CharField(default='No address 1', max_length=80),
        ),
        migrations.AlterField(
            model_name='order',
            name='email',
            field=models.EmailField(default='No email', max_length=128),
        ),
        migrations.AlterField(
            model_name='order',
            name='full_name',
            field=models.CharField(default='No name', max_length=50),
        ),
        migrations.AlterField(
            model_name='order',
            name='phone_number',
            field=models.CharField(default='No phone number', max_length=20),
        ),
    ]

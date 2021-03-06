# Generated by Django 3.1.7 on 2021-03-18 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0004_auto_20210318_1513'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='restaurant',
            name='county',
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='address_2',
            field=models.CharField(blank=True, default='Please enter address', max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='rating',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True),
        ),
    ]

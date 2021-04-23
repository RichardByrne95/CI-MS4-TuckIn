# Generated by Django 3.1.7 on 2021-04-23 13:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0011_auto_20210401_1224'),
        ('checkout', '0005_auto_20210423_1420'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_restaurant',
            field=models.ForeignKey(blank=True, max_length=128, null=True, on_delete=django.db.models.deletion.RESTRICT, to='restaurants.restaurant'),
        ),
    ]

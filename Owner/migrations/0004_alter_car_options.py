# Generated by Django 4.2.1 on 2023-06-23 09:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Owner', '0003_car_created_car_updated'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='car',
            options={'ordering': ['-updated', '-created']},
        ),
    ]

# Generated by Django 4.2.1 on 2023-07-06 08:47

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Hire', '0004_alter_hire_end_date_alter_hire_start_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hire',
            name='end_date',
            field=models.DateField(validators=[django.core.validators.MinValueValidator(datetime.date(2023, 7, 6), 'End date can not be less than today')]),
        ),
        migrations.AlterField(
            model_name='hire',
            name='start_date',
            field=models.DateField(validators=[django.core.validators.MinValueValidator(datetime.date(2023, 7, 6), 'Start date can not be less than today')]),
        ),
    ]

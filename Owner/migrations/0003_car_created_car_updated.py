# Generated by Django 4.2.1 on 2023-06-20 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Owner', '0002_alter_car_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='car',
            name='updated',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]

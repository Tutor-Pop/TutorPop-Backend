# Generated by Django 4.1.2 on 2022-10-06 08:46

import api.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0027_alter_schoolrooms_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservation',
            name='payment_url',
        ),
        migrations.AddField(
            model_name='reservation',
            name='payment_pic',
            field=models.ImageField(default=None, upload_to=api.models.upload_payment),
        ),
    ]
# Generated by Django 4.1.2 on 2022-10-10 08:45

import api.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0030_remove_openrequests_document_url_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='openrequests',
            name='document',
            field=models.FileField(default=None, null=True, upload_to=api.models.upload_payment),
        ),
    ]

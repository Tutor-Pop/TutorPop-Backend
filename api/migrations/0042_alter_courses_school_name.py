# Generated by Django 4.1.2 on 2022-11-10 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0041_remove_courses_payment_method_picture_url_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="courses",
            name="school_name",
            field=models.CharField(default=None, max_length=100, null=True),
        ),
    ]

# Generated by Django 4.1.2 on 2022-11-11 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0046_courses_course_pic"),
    ]

    operations = [
        migrations.AlterField(
            model_name="reservation",
            name="status",
            field=models.CharField(default=None, max_length=30),
        ),
    ]

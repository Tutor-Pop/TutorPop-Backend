# Generated by Django 4.1.1 on 2022-09-22 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_courses_coursetype_schooltypes_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='courses',
            name='type_id',
        ),
        migrations.AddField(
            model_name='courses',
            name='type',
            field=models.CharField(choices=[('NONE', 'NONE'), ('MTH', 'MATH')], default='NONE', max_length=10),
        ),
    ]
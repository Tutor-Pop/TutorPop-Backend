# Generated by Django 4.1.2 on 2022-10-19 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0037_alter_studytime_end_time_alter_studytime_start_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studytimerecords',
            name='end_time',
            field=models.TimeField(blank=True, default=None),
        ),
        migrations.AlterField(
            model_name='studytimerecords',
            name='start_time',
            field=models.TimeField(blank=True, default=None),
        ),
    ]

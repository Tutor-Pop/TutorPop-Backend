# Generated by Django 4.1.1 on 2022-09-26 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0019_schoolrooms_room_descripition'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schoolrooms',
            name='room_descripition',
            field=models.CharField(blank=True, default=None, max_length=1000),
        ),
    ]

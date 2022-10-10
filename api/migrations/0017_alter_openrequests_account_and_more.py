# Generated by Django 4.1.1 on 2022-09-26 09:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_alter_courses_end_date_alter_courses_start_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='openrequests',
            name='account',
            field=models.ForeignKey(db_column='account_id', on_delete=django.db.models.deletion.CASCADE, to='api.account'),
        ),
        migrations.RenameField(
            model_name='openrequests',
            old_name='account',
            new_name='account_id',
        ),
    ]
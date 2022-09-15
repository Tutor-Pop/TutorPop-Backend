# Generated by Django 4.0.6 on 2022-09-13 06:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_delete_item_delete_user_remove_school_owner_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.account')),
                ('school_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.school')),
            ],
        ),
    ]

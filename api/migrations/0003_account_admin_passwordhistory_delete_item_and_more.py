# Generated by Django 4.1.1 on 2022-09-12 07:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_user_description_user_email_user_firstname_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('account_id', models.AutoField(primary_key=True, serialize=False)),
                ('firstname', models.CharField(default='', max_length=50)),
                ('lastname', models.CharField(default='', max_length=50)),
                ('username', models.CharField(max_length=50, unique=True)),
                ('password', models.CharField(default=None, max_length=128)),
                ('email', models.EmailField(default=None, max_length=50)),
                ('year_of_birth', models.IntegerField(blank=True, default=None)),
                ('description', models.CharField(blank=True, default=None, max_length=50)),
                ('is_verified', models.BooleanField(default=False)),
                ('profile_picture', models.CharField(blank=True, default=None, max_length=1000)),
                ('user_status', models.CharField(default=None, max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('admin_id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=50, unique=True)),
                ('password', models.CharField(default=None, max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='PasswordHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(default=None, max_length=128)),
                ('account_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.account')),
            ],
        ),
    ]

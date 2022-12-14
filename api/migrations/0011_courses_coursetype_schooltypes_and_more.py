# Generated by Django 4.1.1 on 2022-09-16 12:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_remove_account_user_status_account_is_deleted'),
    ]

    operations = [
        migrations.CreateModel(
            name='Courses',
            fields=[
                ('course_id', models.AutoField(primary_key=True, serialize=False)),
                ('course_name', models.CharField(default=None, max_length=100)),
                ('type_id', models.CharField(default=None, max_length=100)),
                ('course_description', models.CharField(default=None, max_length=300)),
                ('reserve_open_date', models.DateTimeField(default=None)),
                ('reserve_close_date', models.DateTimeField(default=None)),
                ('start_date', models.DateTimeField(default=None)),
                ('end_date', models.DateTimeField(default=None)),
                ('course_period', models.IntegerField(default=None)),
                ('course_price', models.FloatField(default=None)),
                ('maximum_student', models.IntegerField(default=None)),
                ('reserved_student', models.IntegerField(default=None)),
                ('payment_method_text', models.CharField(blank=True, default=None, max_length=1000)),
                ('payment_method_picture_url', models.CharField(blank=True, default=None, max_length=1000)),
                ('is_deleted', models.BooleanField(default=False)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.account')),
            ],
        ),
        migrations.CreateModel(
            name='CourseType',
            fields=[
                ('type_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(default=None, max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='SchoolTypes',
            fields=[
                ('type_id', models.AutoField(primary_key=True, serialize=False)),
                ('type_name', models.CharField(default=None, max_length=50)),
            ],
        ),
        migrations.RenameField(
            model_name='passwordhistory',
            old_name='account_id',
            new_name='account',
        ),
        migrations.RenameField(
            model_name='school',
            old_name='owner_id',
            new_name='owner',
        ),
        migrations.RenameField(
            model_name='teacher',
            old_name='account_id',
            new_name='account',
        ),
        migrations.RenameField(
            model_name='teacher',
            old_name='school_id',
            new_name='school',
        ),
        migrations.CreateModel(
            name='StudyTimeRecords',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('study_date', models.DateField(blank=True, default=None)),
                ('start_time', models.DateTimeField(blank=True, default=None)),
                ('end_time', models.DateTimeField(blank=True, default=None)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.courses')),
            ],
        ),
        migrations.CreateModel(
            name='StudyTime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(default=None, max_length=3)),
                ('start_time', models.DateTimeField(blank=True, default=None)),
                ('end_time', models.DateTimeField(blank=True, default=None)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.courses')),
            ],
        ),
        migrations.CreateModel(
            name='SchoolWithType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.school')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.schooltypes')),
            ],
        ),
        migrations.CreateModel(
            name='SchoolRooms',
            fields=[
                ('room_id', models.AutoField(primary_key=True, serialize=False)),
                ('room_name', models.CharField(default=None, max_length=100)),
                ('maximum_seat', models.IntegerField(default=None)),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.school')),
            ],
        ),
        migrations.CreateModel(
            name='RoomUsage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.courses')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.schoolrooms')),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('payment_url', models.CharField(blank=True, default=None, max_length=1000)),
                ('status', models.CharField(default=None, max_length=10)),
                ('expire_datetime', models.DateTimeField()),
                ('reservation_datetime', models.DateTimeField()),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.account')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.courses')),
            ],
        ),
        migrations.CreateModel(
            name='OpenRequests',
            fields=[
                ('request_id', models.AutoField(primary_key=True, serialize=False)),
                ('document_url', models.CharField(default=None, max_length=1000)),
                ('requese_timestamp', models.DateTimeField(default=None)),
                ('proof_of_payment_ur', models.CharField(default=None, max_length=1000)),
                ('requesst_status', models.CharField(default=None, max_length=10)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.account')),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.school')),
            ],
        ),
        migrations.CreateModel(
            name='FavCourse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.account')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.courses')),
            ],
        ),
        migrations.CreateModel(
            name='CourseTeacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.account')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.courses')),
            ],
        ),
        migrations.AddField(
            model_name='courses',
            name='school',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.school'),
        ),
        migrations.CreateModel(
            name='CourseHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.account')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.courses')),
            ],
        ),
    ]

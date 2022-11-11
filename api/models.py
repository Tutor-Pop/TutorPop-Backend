from email import message
from pyexpat import model
from django.db import models

from api.constants.choice import CourseTypeChoice


def upload_payment(instance, filename):
    return f"payments/{filename}"


def upload_document(instance, filename):
    return f"documents/{filename}"


def upload_logo(instance, filename):
    return f"logos/{filename}"


def upload_banner(instance, filename):
    return f"banners/{filename}"


def upload_method(instance, filename):
    return f"methods/{filename}"


def upload_profile(instance, filename):
    return f"profile/{filename}"


def upload_poster(instance, filename):
    return f"courses/{filename}"


class Admin(models.Model):
    admin_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128, default=None)


class Account(models.Model):
    account_id = models.AutoField(primary_key=True)
    firstname = models.CharField(max_length=50, default="")
    lastname = models.CharField(max_length=50, default="")
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128, default=None)
    email = models.EmailField(max_length=50, default=None)
    year_of_birth = models.IntegerField(blank=True, default=None)
    description = models.CharField(max_length=50, blank=True, default=None)
    is_verified = models.BooleanField(default=False)
    profile_picture = models.ImageField(
        upload_to=upload_profile, default=None, null=True
    )
    is_deleted = models.BooleanField(default=False)
    token = models.CharField(max_length=256, null=True, default=None)
    token_expire = models.IntegerField(null=True, default=None)
    created_date = models.DateTimeField(auto_now_add=True)


class PasswordHistory(models.Model):
    account_id = models.ForeignKey(
        Account, on_delete=models.CASCADE, db_column="account_id"
    )
    password = models.CharField(max_length=128, default=None)


class School(models.Model):
    school_id = models.AutoField(primary_key=True)
    owner_id = models.ForeignKey(
        Account, on_delete=models.CASCADE, default=1, db_column="owner_id"
    )
    name = models.CharField(max_length=100, default=None)
    description = models.CharField(max_length=300, default=None)
    addr_description = models.CharField(
        max_length=100, default=None, blank=True, null=True
    )
    sub_district = models.CharField(max_length=100, default=None, blank=True, null=True)
    district = models.CharField(max_length=100, default=None, blank=True, null=True)
    province = models.CharField(max_length=100, default=None, blank=True, null=True)
    postal_code = models.CharField(max_length=5, default=None, blank=True, null=True)
    status = models.CharField(max_length=10, default=None, blank=True, null=True)
    logo_pic = models.ImageField(
        upload_to=upload_logo, default=None, blank=True, null=True
    )
    banner_pic = models.ImageField(
        upload_to=upload_banner, default=None, blank=True, null=True
    )


class Teacher(models.Model):
    account_id = models.ForeignKey(
        Account, on_delete=models.CASCADE, db_column="account_id"
    )
    school_id = models.ForeignKey(
        School, on_delete=models.CASCADE, db_column="school_id"
    )


# class CourseType(models.Model):
#     type_id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=50, default=None)


class Courses(models.Model):
    course_id = models.AutoField(primary_key=True)
    school_id = models.ForeignKey(
        School, on_delete=models.CASCADE, db_column="school_id"
    )
    school_name = models.CharField(max_length=100, default=None, null=True)
    owner_id = models.ForeignKey(
        Account, on_delete=models.CASCADE, db_column="owner_id"
    )
    course_name = models.CharField(max_length=100, default=None)
    type = models.CharField(
        max_length=10, choices=CourseTypeChoice.choices, default=CourseTypeChoice.NONE
    )
    course_description = models.CharField(max_length=300, default=None)
    reserve_open_date = models.DateTimeField(default=None)
    reserve_close_date = models.DateTimeField(default=None)
    start_date = models.DateField(default=None)
    end_date = models.DateField(default=None)
    course_period = models.IntegerField(default=None)
    course_price = models.FloatField(default=None)
    maximum_student = models.IntegerField(default=None)
    reserved_student = models.IntegerField(default=None)
    payment_method_text = models.CharField(blank=True, max_length=1000, default=None)
    payment_method_pic = models.ImageField(
        upload_to=upload_method, default=None, blank=True, null=True
    )
    course_pic = models.ImageField(
        upload_to=upload_poster, default=None, blank=True, null=True
    )
    is_deleted = models.BooleanField(default=False)


class Reservation(models.Model):
    id = models.AutoField(primary_key=True)
    course_id = models.ForeignKey(
        Courses, on_delete=models.CASCADE, db_column="course_id"
    )
    account_id = models.ForeignKey(
        Account, on_delete=models.CASCADE, db_column="account_id"
    )
    payment_pic = models.ImageField(upload_to=upload_payment, default=None, null=True)
    status = models.CharField(max_length=30, default=None)
    expire_datetime = models.DateTimeField()
    reservation_datetime = models.DateTimeField()


class CourseHistory(models.Model):
    course_id = models.ForeignKey(
        Courses, on_delete=models.CASCADE, db_column="course_id"
    )
    account_id = models.ForeignKey(
        Account, on_delete=models.CASCADE, db_column="account_id"
    )


class FavCourse(models.Model):
    account_id = models.ForeignKey(
        Account, on_delete=models.CASCADE, db_column="account_id"
    )
    course_id = models.ForeignKey(
        Courses, on_delete=models.CASCADE, db_column="course_id"
    )


class CourseTeacher(models.Model):
    course_id = models.ForeignKey(
        Courses, on_delete=models.CASCADE, db_column="course_id"
    )
    account_id = models.ForeignKey(
        Account, on_delete=models.CASCADE, db_column="account_id"
    )

    class Meta:
        unique_together = ("course_id", "account_id")


class StudyTime(models.Model):
    course_id = models.ForeignKey(
        Courses, on_delete=models.CASCADE, db_column="course_id"
    )
    day = models.CharField(max_length=3, default=None)
    start_time = models.TimeField(blank=True, default=None)
    end_time = models.TimeField(blank=True, default=None)


class StudyTimeRecords(models.Model):
    course_id = models.ForeignKey(
        Courses, on_delete=models.CASCADE, db_column="course_id"
    )
    study_date = models.DateField(blank=True, default=None)
    start_time = models.TimeField(blank=True, default=None)
    end_time = models.TimeField(blank=True, default=None)


class OpenRequests(models.Model):
    request_id = models.AutoField(primary_key=True)
    account_id = models.ForeignKey(
        Account, on_delete=models.CASCADE, db_column="account_id"
    )
    school_id = models.ForeignKey(
        School, on_delete=models.CASCADE, db_column="school_id"
    )
    document = models.FileField(upload_to=upload_document, default=None, null=True)
    request_timestamp = models.DateTimeField(default=None)
    payment_pic = models.ImageField(upload_to=upload_payment, default=None, null=True)
    request_status = models.CharField(max_length=30, default=None)


class SchoolTypes(models.Model):
    type_id = models.AutoField(primary_key=True)
    type_name = models.CharField(max_length=50, default=None)


class SchoolWithType(models.Model):
    type_id = models.ForeignKey(
        SchoolTypes, on_delete=models.CASCADE, db_column="type_id"
    )
    school = models.ForeignKey(School, on_delete=models.CASCADE)


class SchoolRooms(models.Model):
    room_id = models.AutoField(primary_key=True)
    school_id = models.ForeignKey(
        School, on_delete=models.CASCADE, db_column="school_id"
    )
    room_name = models.CharField(max_length=100, default=None)
    maximum_seat = models.IntegerField(default=None)
    description = models.CharField(max_length=1000, default=None)


class RoomUsage(models.Model):
    room_id = models.ForeignKey(
        SchoolRooms, on_delete=models.CASCADE, db_column="room_id"
    )
    course_id = models.ForeignKey(
        Courses, on_delete=models.CASCADE, db_column="course_id"
    )


class Notification(models.Model):
    account_id = models.ForeignKey(
        Account, on_delete=models.CASCADE, db_column="account_id"
    )
    title = models.CharField(max_length=100, null=True, default=None)
    message_noti = models.CharField(max_length=300, default=None)
    create_time = models.DateTimeField(blank=False, null=False, default=None)
    expire_date = models.DateField(blank=True, default=None)

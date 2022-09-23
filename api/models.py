from pyexpat import model
from django.db import models

from api.constants.choice import CourseTypeChoice


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
    profile_picture = models.CharField(
        max_length=1000, blank=True, default=None)
    is_deleted = models.BooleanField(default=False)


class PasswordHistory(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    password = models.CharField(max_length=128, default=None)


class School(models.Model):
    school_id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(
        Account, on_delete=models.CASCADE, default=1)  # เดี๋ยวต้องแก้
    name = models.CharField(max_length=100, default=None)
    description = models.CharField(max_length=300, default=None)
    address = models.CharField(max_length=100, default=None)
    status = models.CharField(max_length=10, default=None)
    logo_url = models.CharField(max_length=1000, default=None)
    banner_url = models.CharField(max_length=1000, default=None)


class Teacher(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE)


# class CourseType(models.Model):
#     type_id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=50, default=None)


class Courses(models.Model):
    course_id = models.AutoField(primary_key=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    owner = models.ForeignKey(Account, on_delete=models.CASCADE)
    course_name = models.CharField(max_length=100, default=None)
    type = models.CharField(
        max_length=10, choices=CourseTypeChoice.choices, default=CourseTypeChoice.NONE)
    course_description = models.CharField(max_length=300, default=None)
    reserve_open_date = models.DateTimeField(default=None)
    reserve_close_date = models.DateTimeField(default=None)
    start_date = models.DateTimeField(default=None)
    end_date = models.DateTimeField(default=None)
    course_period = models.IntegerField(default=None)
    course_price = models.FloatField(default=None)
    maximum_student = models.IntegerField(default=None)
    reserved_student = models.IntegerField(default=None)
    payment_method_text = models.CharField(
        blank=True, max_length=1000, default=None)
    payment_method_picture_url = models.CharField(
        blank=True, max_length=1000, default=None)
    is_deleted = models.BooleanField(default=False)


class Reservation(models.Model):
    id = models.AutoField(primary_key=True)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    payment_url = models.CharField(max_length=1000, blank=True, default=None)
    status = models.CharField(max_length=10, default=None)
    expire_datetime = models.DateTimeField()
    reservation_datetime = models.DateTimeField()


class CourseHistory(models.Model):
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)


class FavCourse(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)


class CourseTeacher(models.Model):
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    class Meta:
        unique_together = ('course','account')


class StudyTime(models.Model):
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    day = models.CharField(max_length=3, default=None)
    start_time = models.DateTimeField(blank=True, default=None)
    end_time = models.DateTimeField(blank=True, default=None)


class StudyTimeRecords(models.Model):
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    study_date = models.DateField(blank=True, default=None)
    start_time = models.DateTimeField(blank=True, default=None)
    end_time = models.DateTimeField(blank=True, default=None)


class OpenRequests(models.Model):
    request_id = models.AutoField(primary_key=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    document_url = models.CharField(max_length=1000, default=None)
    request_timestamp = models.DateTimeField(default=None)
    proof_of_payment_url = models.CharField(max_length=1000, default=None)
    request_status = models.CharField(max_length=10, default=None)


class SchoolTypes(models.Model):
    type_id = models.AutoField(primary_key=True)
    type_name = models.CharField(max_length=50, default=None)


class SchoolWithType(models.Model):
    type = models.ForeignKey(SchoolTypes, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE)


class SchoolRooms(models.Model):
    room_id = models.AutoField(primary_key=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    room_name = models.CharField(max_length=100, default=None)
    maximum_seat = models.IntegerField(default=None)


class RoomUsage(models.Model):
    room = models.ForeignKey(SchoolRooms, on_delete=models.CASCADE)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)

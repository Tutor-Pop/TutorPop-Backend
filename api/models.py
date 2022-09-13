from pyexpat import model
from django.db import models

class Admin(models.Model):
    admin_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50,unique=True)
    password = models.CharField(max_length=128,default=None)

class Account(models.Model):
    account_id = models.AutoField(primary_key=True)
    firstname = models.CharField(max_length=50,default="")
    lastname = models.CharField(max_length=50,default="")
    username = models.CharField(max_length=50,unique=True)
    password = models.CharField(max_length=128,default=None)
    email = models.EmailField(max_length=50,default=None)
    year_of_birth = models.IntegerField(blank=True,default=None)
    description = models.CharField(max_length=50,blank=True,default=None)
    is_verified = models.BooleanField(default=False)
    profile_picture = models.CharField(max_length=1000,blank=True,default=None)
    user_status = models.CharField(max_length=10,default=None)

class PasswordHistory(models.Model):
    account_id = models.ForeignKey(Account,on_delete=models.CASCADE)
    password = models.CharField(max_length=128,default=None)

class School(models.Model):
    school_id = models.AutoField(primary_key=True)
    owner_id = models.ForeignKey(Account,on_delete=models.CASCADE,default=None) # เดี๋ยวต้องแก้
    name = models.CharField(max_length=100,default=None)
    description = models.CharField(max_length=300,default=None)
    address = models.CharField(max_length=100,default=None)
    status = models.CharField(max_length=10,default=None)
    logo_url = models.CharField(max_length=1000,default=None)
    banner_url = models.CharField(max_length=1000,default=None)

# class Teacher(models.Model):
#     school_id = models.ForeignKey()
#     account_id = models.ForeignKey()

# class Reservation(models.Model):
#     id = models.AutoField(primary_key=True)
#     course = models.ForeignKey()
#     account = models.ForeignKey()
#     payment_url = models.CharField(max_length=1000,blank=True,default=None)
#     status = models.CharField(max_length=10,default=None)
#     expire_datetime = models.DateTimeField()
#     reservation_datetime = models.DateTimeField()

# class CourseHistory(models.Model):
#     course = models.ForeignKey()
#     account = models.ForeignKey()

# class CourseType(models.Model):
#     type_id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=50,default=None)

# class FavCourse(models.Model):
#     account = models.ForeignKey()
#     course = models.ForeignKey()

# class CourseTeacher(models.Model):
#     course = models.ForeignKey()
#     account = models.ForeignKey()

# class Courses(models.Model):
#     course_id = models.AutoField(primary_key=True)
#     school = models.ForeignKey()
#     owner = models.ForeignKey()
#     course_name = models.CharField(max_length=100,default=None)
#     type_id = models.CharField(max_length=100,default=None)
#     course_description = models.CharField(max_length=300,default=None)
#     reserve_open_date = models.DateTimeField(default=None)
#     reserve_close_date = models.DateTimeField(default=None)
#     start_date = models.DateTimeField(default=None)
#     end_date = models.DateTimeField(default=None)
#     course_period = models.IntegerField(default=None)
#     course_price = models.FloatField(default=None)
#     maximum_student = models.IntegerField(default=None)
#     reserved_student = models.IntegerField(default=None)
#     payment_method_text = models.CharField(blank=True,max_length=1000,default=None)
#     payment_method_picture_url = models.CharField(blank=True,max_length=1000,default=None)
#     is_deleted = models.BooleanField(default=False)
    
# class StudyTime(models.Model):
#     course = models.ForeignKey()
#     day = models.CharField(max_length=3,default=None)
#     start_time = models.DateTimeField(blank=True,default=None)
#     end_time = models.DateTimeField(blank=True,default=None)
    
# class StudyTimeRecords(models.Model):
#     course = models.ForeignKey()
#     study_date = models.DateField(blank=True,default=None)
#     start_time = models.DateTimeField(blank=True,default=None)
#     end_time = models.DateTimeField(blank=True,default=None)
class OpenRequests(models.model):
    request_id = models.AutoField(primary_key=True)
    account = models.ForeignKey()
    school = models.ForeignKey()
    document_url = models.CharField(max_length=1000,default=None)
    requese_timestamp = models.DateTimeField(default=None)
    proof_of_payment_ur = models.CharField(max_length=1000,default=None)
    requesst_status = models.CharField(max_length=10,default=None)

class SchoolWithType(models.model):
    type = models.ForeignKey()
    school = models.ForeignKey()

class SchoolTypes(models.model):
    type_id = models.AutoField(primary_key=True)
    type_name = models.CharField(max_length=50,default=None)

class SchoolRooms(models.model):
    room_id = models.AutoField(primary_key=True)
    school = models.ForeignKey()
    room_name = models.CharField(max_length=100,default=None)
    maximum_seat = models.IntegerField(default=None)

class RoomUsage(models.model):
    room = models.ForeignKey()
    course = models.ForeignKey()

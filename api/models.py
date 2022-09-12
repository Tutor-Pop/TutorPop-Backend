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
    owner_id = models.ManyToManyField(Account)
    name = models.CharField(max_length=100,default=None)
    description = models.CharField(max_length=300,default=None)
    address = models.CharField(max_length=100,default=None)
    status = models.CharField(max_length=10,default=None)
    logo_url = models.CharField(max_length=1000,default=None)
    banner_url = models.CharField(max_length=1000,default=None)

# class Teacher(models.Model):
#     school_id = models.ForeignKey()
#     account_id = models.ForeignKey()
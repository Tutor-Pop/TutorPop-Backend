from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    firstname = models.CharField(max_length=50,default="")
    lastname = models.CharField(max_length=50,default="")
    username = models.CharField(max_length=50,unique=True)
    password = models.CharField(max_length=128,default=None)
    email = models.CharField(max_length=50,default=None)
    year_of_birth = models.IntegerField(blank=True,default=None)
    description = models.CharField(max_length=50,blank=True,default=None)
    is_verified = models.BooleanField(default=False)
    profile_picture = models.CharField(max_length=1000,blank=True,default=None)
    user_status = models.CharField(max_length=10,default=None)
from django.urls import path
from . import false_views
from .views import user

urlpatterns = [
    path('',false_views.getData),
    path('register',user.register)
]
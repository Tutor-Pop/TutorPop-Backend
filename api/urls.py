from django.urls import path
from . import false_views
from .views import account

urlpatterns = [
    path('',false_views.getData),
    path('register',account.register),
    path('account',account.get_all_accounts),
    path('account/<int:id>',account.get_delete_account),
    path('account/<int:id>/password',account.change_password),
    path('account/<int:id>/school',account.create_school),
]
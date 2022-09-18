from django.urls import path
from .views import test,account

urlpatterns = [
    #--- 1. Account ---#
    path('register',account.register),
    path('account',account.get_all_accounts),
    path('account/<int:id>',account.get_edit_delete_account),
    path('account/<int:id>/password',account.change_password),
    path('account/<int:id>/school',account.create_school),
]
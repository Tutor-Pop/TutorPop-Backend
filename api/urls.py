from django.urls import path
from .views import auth,account,test

urlpatterns = [
    #--- Authentication ---#
    path('register',auth.register),
    #--- 1. Account ---#
    path('accounts',account.get_all_accounts),
    path('account/<int:id>',account.get_edit_delete_account),
    path('account/<int:id>/password',account.change_password),
    path('account/<int:id>/school',account.create_school),

    path('test',test.get_acounts),
    path('test/<int:id>/edit',test.edit_account),
]
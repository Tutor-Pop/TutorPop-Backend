from django.urls import path
from .views import auth,account,course,room,test

urlpatterns = [
    #--- Authentication ---#
    path('register',auth.register),
    #--- 1. Account ---#
    path('accounts',account.get_all_accounts),
    path('account/<int:id>',account.get_edit_delete_account),
    path('account/<int:id>/password',account.change_password),
    path('account/<int:id>/school',account.create_school),
    #--- 3. Course ---#
    #path('course/<int:course_id>',course.get_course),
    path('school/<int:school_id>/course',course.create_course),
    #--- 5. Room ---#
    path('school/<int:school_id>/room',room.create_room),
    path('school/<int:school_id>/rooms',room.get_all_room_in_school),
    path('school/<int:school_id>/room/<int:room_id>',room.get_update_room),
    #--- Demo ---#
    path('test',test.get_acounts),
    path('test/<int:id>/edit',test.edit_account),
]
from django.urls import path
from .views import auth, account, course, room, test, request, search, school

urlpatterns = [
    #--- Authentication ---#
    path('register', auth.register),
    #--- 1. Account ---#
    path('accounts', account.get_all_accounts),
    path('account/<int:id>', account.get_edit_delete_account),
    path('account/<int:id>/password', account.change_password),
    path('account/<int:id>/school', account.create_school),
    #--- 2.Search ---#
    path('courses/list', search.api_course_search.as_view()),
    #--- 3. Course ---#
    # path('course/<int:course_id>',course.get_course),
    path('schools/<int:school_id>/courses', course.create_course),
    path('schools/<int:school_id>/courses/<int:course_id>',
         course.get_update_course),
    path('schools/<int:school_id>/courses/<int:course_id>/students',
         course.get_student),
    #--- 4. School ---#
    path('school',school.create_school),
    path('school/<int:school_ID>',school.get_edit_delete_school),
    path('school/<int:school_ID>/teachers',school.get_add_delete_teacher),
    #--- 5. Room ---#
    path('schools/<int:school_id>/room', room.create_room),
    path('schools/<int:school_id>/rooms', room.get_all_room_in_school),
    path('schools/<int:school_id>/room/<int:room_id>', room.get_update_room),
    #--- 6. Request ---#
    path('requests', request.get_create_request),
    path('requests/<int:req_id>', request.get_del_update_request),
    #--- Demo ---#
    path('test', test.get_acounts),
    path('test/<int:id>/edit', test.edit_account),
]

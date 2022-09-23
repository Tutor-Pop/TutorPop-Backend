from django.urls import path
from .views import auth, account, course, room, test, request, reservation

urlpatterns = [
    #--- Authentication ---#
    path('register', auth.register),
    #--- 1. Account ---#
    path('accounts', account.get_all_accounts),
    path('accounts/<int:id>', account.get_edit_delete_account),
    path('accounts/<int:id>/password', account.change_password),
    path('accounts/<int:id>/school', account.create_school),
    #--- 3. Course ---#
    # path('course/<int:course_id>',course.get_course),
    path('schools/<int:school_id>/course', course.create_course),
    #--- 5. Room ---#
    path('schools/<int:school_id>/room', room.create_room),
    path('schools/<int:school_id>/rooms', room.get_all_room_in_school),
    path('schools/<int:school_id>/room/<int:room_id>', room.get_update_room),
    #--- 6. Request ---#
    path('requests', request.get_create_request),
    path('requests/<int:req_id>', request.get_del_update_request),
    #-- 7.Reservation --#
    path('reservations', reservation.create_reservation),
    path('reservations/<int:resv_id>', reservation.get_del_reservation),
    path('courses/<course_id>/reservations',
         reservation.get_course_reservations),
    path('reservations/<int:resv_id>/status',
         reservation.update_reservation_status),
    #--- Demo ---#
    path('test', test.get_acounts),
    path('test/<int:id>/edit', test.edit_account),
]

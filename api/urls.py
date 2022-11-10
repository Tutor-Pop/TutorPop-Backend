from django.urls import path
from .views import (
    auth,
    account,
    course,
    room,
    test,
    request,
    search,
    school,
    reservation,
    notification,
    personal,
    stat,
)

urlpatterns = [
    #--- Authentication ---#
    path('register', auth.register),
    path('login', auth.login),
    path('logout', auth.logout),
    path('verify', auth.get_authorization),
    # login already
    #--- 1. Account ---#
    path('accounts', account.get_all_accounts),
    path('accounts/<int:id>', account.get_edit_delete_account),
    path('accounts/<int:id>/password', account.change_password),
    #--- 2.Search ---#
    path('courses/search', search.api_course_search.as_view()),
    path('schools/search', search.api_school_search.as_view()),
    #--- 3. Course ---#
    path('schools/<int:school_id>/courses', course.create_getall_course),
    path('schools/<int:school_id>/courses/<int:course_id>',course.get_update_course),
    path('schools/<int:school_id>/courses/<int:course_id>/students',course.get_student),
    path('schools/<int:school_id>/courses/<int:course_id>/teachers',course.get_update_teachers),
    #--- 4. School ---#
    path('schools', school.create_school),
    path('schools/<int:school_id>', school.get_edit_delete_school),
    path('schools/<int:school_id>/teachers', school.get_add_delete_teacher),
    path('schools/<int:school_id>/status',  school.edit_status_school),
    #--- 5. Room ---#
    path('schools/<int:school_id>/rooms', room.create_getall_room),
    path('schools/<int:school_id>/rooms/<int:room_id>', room.get_update_delete_room),
    path('rooms/<int:room_id>/usages', room.get_room_usage),
    #--- 6. Open Request ---#
    path('requests', request.get_create_request.as_view()),
    path('requests/<int:req_id>', request.get_del_update_request),
    path('requests/<int:req_id>/status', request.update_request_status),
    #--- 7.Reservation --#
    path('reservations', reservation.CreateReserve.as_view()),
    path('courses/<course_id>/reservations', reservation.get_course_reservations),
    path('reservations/<resv_id>/status',reservation.update_reservation_status),
    path('reservations/<int:resv_id>',reservation.get_del_reservation),
    path('reservations/<resv_id>/payment',reservation.UploadPayment.as_view()),
    # --- 8. Personal ---#
    path("accounts/<int:account_id>/reservations", personal.get_my_reserve),
    path("accounts/<int:account_id>/courses", personal.get_reserve),
    path("accounts/<int:account_id>/teachings", personal.get_all_teachings),
    path("accounts/<int:account_id>/times", personal.get_times_ts),
    path("accounts/<int:account_id>/schools", personal.get_schools_member),
    path("accounts/<int:account_id>/owners", personal.get_schools_owner),
    #--- 10. Notification ---#
    path('messages', notification.create_notification),
    path('accounts/<int:account_id>/messages', notification.get_all_notification),
    path('accounts/<int:account_id>/messages_nxp', notification.get_notexpire_notification),
    #--- 11. Stats ---#
    path('stats/active',stat.get_active_stat),
    #--- Demo ---#
    #path('test', test.get_acounts),
    #path('test/<int:id>/edit', test.edit_account),
]
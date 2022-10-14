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
)

urlpatterns = [
    # --- Authentication ---#
    path("register", auth.register),
    # --- 1. Account ---#
    path("accounts", account.get_all_accounts),
    path("accounts/<int:id>", account.get_edit_delete_account),
    # --- 2.Search ---#
    path("courses/search", search.api_course_search.as_view()),
    path("schools/search", search.api_school_search.as_view()),
    # --- 3. Course ---#
    # path('course/<int:course_id>',course.get_course),
    path("schools/<int:school_id>/courses", course.create_course),
    path("schools/<int:school_id>/courses/<int:course_id>", course.get_update_course),
    path(
        "schools/<int:school_id>/courses/<int:course_id>/students", course.get_student
    ),
    # --- 4. School ---#
    path("schools", school.create_school),
    path("schools/<int:school_ID>", school.get_edit_delete_school),
    path("schools/<int:school_ID>/teachers", school.get_add_delete_teacher),
    path("schools/<int:school_ID>/status", school.edit_status_school),
    # path("schools/<int:school_id>/courses", school.get_all_courses),
    # --- 5. Room ---#
    path("schools/<int:school_id>/rooms", room.create_getall_room),
    path("schools/<int:school_id>/rooms/<int:room_id>", room.get_update_delete_room),
    # --- 6. Request ---#
    path("requests", request.get_create_request.as_view()),
    path("requests/<int:req_id>", request.get_del_update_request),
    path("requests/<int:req_id>/status", request.update_request_status),
    # --- 7.Reservation --#
    path("reservations", reservation.CreateReserve.as_view()),
    path("courses/<course_id>/reservations", reservation.get_course_reservations),
    path("reservations/<resv_id>/status", reservation.update_reservation_status),
    path("reservations/<int:resv_id>", reservation.get_del_reservation),
    path("reservations/<resv_id>/payment", reservation.UploadPayment.as_view()),
    # --- 10. Notification ---#
    path("messages", notification.create_notification),
    path("accounts/<int:account_ID>/messages", notification.get_all_notification),
    path(
        "accounts/<int:account_ID>/messages_nxp",
        notification.get_notexpire_notification,
    ),
    # --- Demo ---#
    # path('test', test.get_acounts),
    # path('test/<int:id>/edit', test.edit_account),
]

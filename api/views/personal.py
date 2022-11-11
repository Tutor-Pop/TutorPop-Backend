from unittest import result

from django.forms import model_to_dict
from ..utility import JSONParser, JSONParserOne, passwordEncryption
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..constants.method import GET, POST, PUT, DELETE
from ..models import (
    Reservation,
    CourseTeacher,
    Courses,
    School,
    StudyTime,
    Teacher,
    Account,
)
from rest_framework import status
from ..serializers import (
    CourseSerializer,
    SchoolSerializer,
    AccountSerializer,
    ReservationSerializer,
    AccountSerializer_noT,
)


@api_view([GET])
def get_my_reserve(request, account_id: int):
    account = Reservation.objects.filter(account_id=account_id)
    reservations = JSONParser(account)
    for reserve in reservations:
        cid = reserve["course_id_id"]
        course = Courses.objects.get(course_id=cid)
        sid = course.school_id.school_id
        reserve["school_id"] = sid
    count = len(reservations)
    if count != 0:
        return Response(
            {"count": count, "reservations": reservations}, status=status.HTTP_200_OK
        )
    else:
        return Response({"message": "No reservation"}, status=status.HTTP_404_NOT_FOUND)


# get courses that account study in
@api_view([GET])
def get_reserve(request, account_id: int):
    courses = Courses.objects.filter(
        reservation__account_id=account_id, reservation__status="Confirmed"
    )
    serializer = CourseSerializer(courses)
    count = len(serializer.data)

    return Response(
        {"count": count, "courses": serializer.data}, status=status.HTTP_200_OK
    )


@api_view([GET])
def get_all_teachings(request, account_id: int):
    teacher = Courses.objects.filter(courseteacher__account_id=account_id)
    courses = JSONParser(teacher)
    count = len(courses)
    if count != 0:
        return Response({"count": count, "courses": courses}, status=status.HTTP_200_OK)
    else:
        return Response({"message": "Not Teachings"}, status=status.HTTP_404_NOT_FOUND)


@api_view([GET])
def get_times_ts(request, account_id: int):
    studytime = StudyTime(account__account_id=account_id)

    return Response(model_to_dict(studytime), status=status.HTTP_404_NOT_FOUND)


@api_view([GET])
def get_schools_member(request, account_id: int):
    teach_school = School.objects.filter(teacher__account_id=account_id)
    schools = JSONParser(teach_school)
    count = len(schools)
    if count != 0:
        return Response({"count": count, "schools": schools}, status=status.HTTP_200_OK)
    else:
        return Response(
            {"message": "Not teach in school"}, status=status.HTTP_404_NOT_FOUND
        )


@api_view([GET])
def get_schools_owner(request, account_id: int):
    owner = School.objects.filter(owner_id=account_id)
    schools = JSONParser(owner)
    count = len(schools)
    if count != 0:
        return Response({"count": count, "schools": schools}, status=status.HTTP_200_OK)
    else:
        return Response({"message": "Not Owner"}, status=status.HTTP_404_NOT_FOUND)


@api_view([GET])
def get_teacher_detail(request, user_id: int):
    account = Account.objects.get(account_id=user_id)
    accserial = AccountSerializer_noT(account)
    courses = Courses.objects.filter(courseteacher__account_id=user_id)
    courseserial = CourseSerializer(courses, many=True)
    modified_data = accserial.data
    modified_data["all_courses"] = {
        "count": len(courseserial.data),
        "courses": courseserial.data,
    }
    schools = School.objects.filter(teacher__account_id=user_id)
    schoolserial = SchoolSerializer(schools, many=True)
    modified_data["all_schools"] = {
        "count": len(schoolserial.data),
        "schools": schoolserial.data,
    }
    return Response(modified_data, status=status.HTTP_200_OK)


@api_view([GET])
def get_specific_reserve_course(request, reserve_id: int):
    try:
        reserve = Reservation.objects.get(id=reserve_id)
        course = reserve.course_id
        reserializer = ReservationSerializer(reserve)
        coserializer = CourseSerializer(course)
        return Response(
            {"result": {"reservation": reserializer.data, "course": coserializer.data}},
            status=status.HTTP_200_OK,
        )
    except Reservation.DoesNotExist:
        return Response(
            {"message": "Reservation does not exist"}, status=status.HTTP_404_NOT_FOUND
        )

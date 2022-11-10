from unittest import result

from django.forms import model_to_dict
from ..utility import JSONParser, JSONParserOne, passwordEncryption
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..constants.method import GET, POST, PUT, DELETE
from ..models import Reservation, CourseTeacher, Courses, School, StudyTime, Teacher
from rest_framework import status


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


@api_view([GET])
def get_reserve(request, account_id: int):
    account = Reservation.objects.filter(account_id=account_id, status="Confirmed")
    courses = JSONParser(account)
    count = len(courses)
    if count != 0:
        return Response({"count": count, "courses": courses}, status=status.HTTP_200_OK)
    else:
        return Response({"message": "Not found"}, status=status.HTTP_404_NOT_FOUND)


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

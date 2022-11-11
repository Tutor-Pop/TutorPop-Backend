from ..utility import JSONParser, JSONParserOne
from ..serializers import CourseSerializer, SchoolSerializer, AccountSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes
from ..constants.method import GET, POST, PUT, DELETE
from ..models import (
    Account,
    CourseTeacher,
    PasswordHistory,
    Reservation,
    RoomUsage,
    School,
    Courses,
    SchoolRooms,
    StudyTime,
    StudyTimeRecords,
)
from rest_framework import status
import datetime
import django.db.utils
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.parsers import JSONParser as JP
from django.utils import timezone


@api_view([GET, PUT, DELETE])
def get_update_course(request, course_id: int):
    try:
        course = Courses.objects.get(course_id=course_id, is_deleted=False)

        if request.method == GET:
            serializer = CourseSerializer(course)
            return Response({"result": serializer.data}, status=status.HTTP_200_OK)

        elif request.method == PUT:
            serializer = CourseSerializer(course, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"result": serializer.data}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == DELETE:
            course.is_deleted = True
            course.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

    except Courses.DoesNotExist:
        return Response(
            {"message": "Course doesn't not exists!"}, status=status.HTTP_404_NOT_FOUND
        )


@api_view([GET, PUT, DELETE])
def get_update_teachers(request, course_id: int):
    try:
        course = Courses.objects.get(course_id=course_id, is_deleted=False)
        teacher = Account.objects.filter(courseteacher__course_id=course_id)

        if request.method == GET:
            serializer = AccountSerializer(teacher, many=True)
            return Response({"result": serializer.data}, status=status.HTTP_200_OK)

        elif request.method == PUT:
            for i in request.data["teacher_id"]:
                try:
                    account = Account.objects.get(account_id=i)
                    courseteacher = CourseTeacher(account_id=account, course_id=course)
                    courseteacher.save()
                except:
                    pass

            return Response(
                {"message": "Update Successfully"}, status=status.HTTP_200_OK
            )

        elif request.method == DELETE:
            for i in request.data["teacher_id"]:
                try:
                    deletecourse = CourseTeacher.objects.get(
                        course_id=course_id, account_id=i
                    )
                    deletecourse.delete()
                except:
                    pass

            return Response(
                {"message": "Update Successfully"}, status=status.HTTP_204_NO_CONTENT
            )

    except Courses.DoesNotExist:
        return Response(
            {"message": "Course doesn't not exists!"}, status=status.HTTP_404_NOT_FOUND
        )


@api_view([GET])
def get_student(request, course_id: int):
    try:
        Courses.objects.get(course_id=course_id, is_deleted=False)

        student = Account.objects.filter(reservation__course_id=course_id)
        serializer = AccountSerializer(student, many=True)
        return Response({"result": serializer.data}, status=status.HTTP_200_OK)

    except Courses.DoesNotExist:
        return Response(
            {"message": "Course doesn't not exists!"}, status=status.HTTP_404_NOT_FOUND
        )


@api_view([POST, GET])
def create_getall_course(request, school_id: int):
    if request.method == POST:
        school = School.objects.get(school_id=school_id)
        room = SchoolRooms.objects.get(room_id=request.data["room_id"])
        print(request.data)
        # owner = Account.objects.get(account_id=request.data["owner_id"])
        modified_data = request.data
        print(school.name)
        modified_data["school_name"] = school.name
        modified_data["school_id"] = school_id
        serializer = CourseSerializer(data=modified_data, partial=True)
        if serializer.is_valid():
            # print(serializer.data)
            serializer.save()
            course_id = serializer.data["course_id"]
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        course = Courses.objects.get(course_id=course_id)
        roomusage = RoomUsage(room_id=room, course_id=course)
        roomusage.save()

        for i in request.data["study_time"]:
            study_time = StudyTime(
                course_id=course,
                day=i["day"],
                start_time=i["start_time"],
                end_time=i["end_time"],
            )
        study_time.save()
        for i in request.data["teachers"]:
            try:
                account = Account.objects.get(account_id=i)
                courseteacher = CourseTeacher(account_id=account, course_id=course)
                courseteacher.save()
            except:
                pass
        # for i in request.data["study_time_record"]:
        #    study_time_record = StudyTimeRecords(
        #        course_id=course,
        #        study_date=i["study_date"],
        #        start_time=i["start_time"],
        #        end_time=i["end_time"],
        #    )
        #    study_time_record.save()

        return Response(
            {"message": "Course created successfully", "result": serializer.data},
            status=status.HTTP_201_CREATED,
        )

    if request.method == GET:
        try:
            school = School.objects.get(school_id=school_id)
        except School.DoesNotExist:
            return Response(
                {"message": "School does not exists!"},
                status=status.HTTP_404_NOT_FOUND,
            )

        all_courses = Courses.objects.filter(
            school_id=school_id, end_date__gt=timezone.now().date()
        )
        serializer = CourseSerializer(all_courses, many=True)
        return Response(
            {"count": len(serializer.data), "result": serializer.data},
            status=status.HTTP_200_OK,
        )


@api_view([PUT])
@parser_classes([MultiPartParser, FormParser, JP])
def upload_method_pic(request, course_id: int):
    try:
        course = Courses.objects.get(course_id=course_id)
    except Courses.DoesNotExist:
        return Response(
            {"message": "Course does not exists!"},
            status=status.HTTP_404_NOT_FOUND,
        )
    if request.method == "PUT":
        serializer = CourseSerializer(course, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"result": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view([GET])
def populate_all_course(request):
    courses = Courses.objects.all()
    serializer = CourseSerializer(courses, many=True)
    for course in serializer.data:
        sid = course["school_id"]
        oid = course["owner_id"]
        school = School.objects.get(school_id=sid)
        owner = Account.objects.get(account_id=oid)
        schoolserial = SchoolSerializer(school)
        course["school_detail"] = schoolserial.data
        ownerserial = AccountSerializer(owner)
        course["owner_detail"] = ownerserial.data
    return Response(
        {"count": len(serializer.data), "result": serializer.data},
        status=status.HTTP_200_OK,
    )


@api_view([PUT])
@parser_classes([MultiPartParser, FormParser, JP])
def upload_course_pic(request, course_id: int):
    try:
        course = Courses.objects.get(course_id=course_id)
    except Courses.DoesNotExist:
        return Response(
            {"message": "Course does not exists!"},
            status=status.HTTP_404_NOT_FOUND,
        )
    if request.method == "PUT":
        serializer = CourseSerializer(course, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"result": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

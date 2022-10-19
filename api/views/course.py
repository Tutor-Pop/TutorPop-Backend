from ..utility import JSONParser, JSONParserOne
from ..serializers import CourseSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
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
    StudyTimeRecords
)
from rest_framework import status
import datetime
import django.db.utils


@api_view([GET, PUT, DELETE])
def get_update_course(request, school_id: int, course_id: int):
    try:
        school = School.objects.get(school_id=school_id)
        course = Courses.objects.get(
            course_id=course_id, school_id=school_id, is_deleted=False
        )

        if request.method == GET:
            result = JSONParserOne(course)
            return Response({"result": result}, status=status.HTTP_200_OK)

        elif request.method == PUT:
            serializer = CourseSerializer(course, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == DELETE:
            course.is_deleted = True
            course.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

    except Courses.DoesNotExist:
        return Response(
            {"message": "Course doesn't not exists!"}, status=status.HTTP_404_NOT_FOUND
        )
    except School.DoesNotExist:
        return Response(
            {"message": "School doesn't not exists!"}, status=status.HTTP_404_NOT_FOUND
        )


@api_view([GET, PUT, DELETE])
def get_update_teachers(request, school_id: int, course_id: int):
    try:
        school = School.objects.get(school_id=school_id)
        course = Courses.objects.get(
            course_id=course_id, school_id=school_id, is_deleted=False
        )
        teacher = Account.objects.filter(courseteacher__course_id=course_id)

        if request.method == GET:
            result = JSONParser(teacher)
            return Response({"result": result}, status=status.HTTP_200_OK)

        elif request.method == PUT:
            for i in request.data["teacher_id"]:
                try:
                    account = Account.objects.get(account_id=i)
                    courseteacher = CourseTeacher(
                        account_id=account,course_id=course)
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
    except School.DoesNotExist:
        return Response(
            {"message": "School doesn't not exists!"}, status=status.HTTP_404_NOT_FOUND
        )


@api_view([GET])
def get_student(request, school_id: int, course_id: int):
    try:
        School.objects.get(school_id=school_id)
        Courses.objects.get(course_id=course_id, school_id=school_id, is_deleted=False)

        student = Account.objects.filter(reservation__course_id=course_id)
        return Response({"result": JSONParser(student)}, status=status.HTTP_200_OK)

    except Courses.DoesNotExist:
        return Response(
            {"message": "Course doesn't not exists!"}, status=status.HTTP_404_NOT_FOUND
        )
    except School.DoesNotExist:
        return Response(
            {"message": "School doesn't not exists!"}, status=status.HTTP_404_NOT_FOUND
        )


@api_view([POST, GET])
def create_course(request, school_id: int):
    if request.method == POST:
        school = School.objects.get(school_id=school_id)
        room = SchoolRooms.objects.get(room_id=request.data["room_id"])
        owner = Account.objects.get(account_id=request.data["owner_id"])
        course = Courses(
            school_id=school,
            owner_id=owner,
            course_name=request.data["course_name"],
            type=request.data["type"],
            course_description=request.data["course_description"],
            reserve_open_date=request.data["reserve_open_date"],
            reserve_close_date=request.data["reserve_close_date"],
            start_date=request.data["start_date"],
            end_date=request.data["end_date"],
            course_period=request.data["course_period"],
            course_price=request.data["course_price"],
            maximum_student=request.data["maximum_student"],
            reserved_student=0,
            payment_method_text=request.data["payment_method_text"],
            payment_method_picture_url=request.data["payment_method_picture_url"],
        )
        course.save()

        roomusage = RoomUsage(room_id=room, course_id=course)
        roomusage.save()

        
        for i in request.data["study_time"]:
            study_time = StudyTime(
                course_id = course,
                day = i["day"],
                start_time = i["start_time"],
                end_time = i["end_time"]
            )
            study_time.save()
    
        for i in request.data['study_time_record']:
            study_time_record = StudyTimeRecords(
                course_id = course,
                study_date = i["study_date"],
                start_time = i["start_time"],
                end_time = i["end_time"]
            )
            study_time_record.save()

        return Response(
            {"message": "Course created successfully", "result": JSONParserOne(course)},
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
            school_id=school_id, end_date__gt=datetime.date.today()
        )
        serializer = CourseSerializer(all_courses, many=True)
        return Response(
            {"count": len(serializer.data), "result": serializer.data},
            status=status.HTTP_200_OK,
        )

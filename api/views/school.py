from functools import partial
from ..models import Account, Courses, PasswordHistory, School, Teacher

from cgitb import reset
from ..utility import JSONParser, JSONParserOne, passwordEncryption
from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes
from ..constants.method import GET, POST, PUT, DELETE
from ..models import Account, PasswordHistory, School, Teacher
from rest_framework import status
from ..serializers import (
    SchoolSerializer,
    SchoolStatusSerializer,
    CourseSerializer,
    AccountSerializer,
)
from rest_framework.generics import ListAPIView
from rest_framework.parsers import MultiPartParser, FormParser


@api_view([POST])
@parser_classes([MultiPartParser, FormParser])
def create_school(request):
    serializer = SchoolSerializer(data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view([GET, PUT, DELETE])
@parser_classes([MultiPartParser, FormParser])
def get_edit_delete_school(request, school_id: int):
    if request.method == GET:
        try:
            result = JSONParserOne(School.objects.get(school_id=school_id))
            return Response({"result": result}, status=status.HTTP_200_OK)
        except:
            return Response(
                {"message": "School doesn't exist!"}, status=status.HTTP_404_NOT_FOUND
            )
    elif request.method == PUT:
        try:
            school = School.objects.get(school_id=school_id)
            serializer = SchoolSerializer(school, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    elif request.method == DELETE:
        try:
            school = School.objects.get(school_id=school_id)
            school.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response("School not found!", status=status.HTTP_404_NOT_FOUND)


@api_view([GET, PUT, DELETE])
def get_add_delete_teacher(request, school_id: int):
    # ต้องแยกประเภทไหมว่าหาอะไรไม่เจอ
    if request.method == GET:
        try:
            school = School.objects.get(school_id=school_id)
            account = Account.objects.filter(teacher__school_id=school_id)
            result = JSONParser(account)
            return Response({"teachers": result})
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    elif request.method == PUT:
        try:
            teachers = request.data["teachers"]
            tmpSchool = School.objects.get(school_id=school_id)
            for i in teachers:
                tmpAcc = Account.objects.get(account_id=i)
                Teacher.objects.get_or_create(account_id=tmpAcc, school_id=tmpSchool)
            all_teachers = Teacher.objects.filter(school_id=school_id)
            result = JSONParser(all_teachers)  # แสดงผลครูทั้งหมดในโรงเรียน
            return Response({"teachers": result}, status=status.HTTP_200_OK)
        except:
            # ถ้าใส่ "teachers":[1,5] จะเพิ่ม 1 แต่ไม่เพิ่ม 5
            return Response(
                "Account or School Not Found", status=status.HTTP_404_NOT_FOUND
            )
    elif request.method == DELETE:
        try:
            teachers = request.data["teachers"]
            for i in teachers:
                Teacher.objects.filter(account_id=i, school_id=school_id).delete()
            all_teachers = Teacher.objects.filter(school_id=school_id)
            result = JSONParser(all_teachers)  # แสดงผลครูทั้งหมดในโรงเรียน
            return Response({"teachers": result}, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view([PUT])
def edit_status_school(request, school_id: int):
    try:
        school = School.objects.get(school_id=school_id)
        serializer = SchoolStatusSerializer(school, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response({"result": serializer.data}, status=status.HTTP_200_OK)
    except:
        return Response({"result": {}}, status=status.HTTP_404_NOT_FOUND)


@api_view([GET])
def get_all_others(request, school_id: int):
    try:
        school = School.objects.get(school_id=school_id)
    except:
        return Response({"result": {}}, status=status.HTTP_404_NOT_FOUND)
    others = Account.objects.exclude(teacher__school_id=school_id).exclude(
        school__school_id=school_id
    )
    result = JSONParser(others)
    return Response({"others": result}, status=status.HTTP_200_OK)


@api_view([GET])
def get_school_details(request, school_id: int):
    try:
        school = School.objects.get(school_id=school_id)
    except:
        return Response({"result": {}}, status=status.HTTP_404_NOT_FOUND)
    schoolserial = SchoolSerializer(school)
    modified_data = schoolserial.data
    accounts = Account.objects.filter(teacher__school_id=school_id)
    accserial = AccountSerializer(accounts, many=True)
    modified_data["all_teachers"] = {
        "count": len(accserial.data),
        "teachers": accserial.data,
    }
    courses = Courses.objects.filter(school_id=school_id)
    courseserial = CourseSerializer(courses, many=True)
    modified_data["all_courses"] = {
        "count": len(courseserial.data),
        "courses": courseserial.data,
    }
    return Response(modified_data, status=status.HTTP_200_OK)

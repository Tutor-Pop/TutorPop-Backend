from ..models import Account, Courses, PasswordHistory, School, Teacher

from cgitb import reset
from ..utility import JSONParser, JSONParserOne, passwordEncryption
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..constants.method import GET, POST, PUT, DELETE
from ..models import Account, PasswordHistory, School, Teacher
from rest_framework import status
from ..serializers import SchoolSerializer, SchoolStatusSerializer, CourseSerializer
from rest_framework.generics import ListAPIView


@api_view([POST])
def create_school(request):
    serializer = SchoolSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view([GET, PUT, DELETE])
def get_edit_delete_school(request, school_ID: int):
    if request.method == GET:
        try:
            result = JSONParserOne(School.objects.get(school_id=school_ID))
            return Response({"result": result}, status=status.HTTP_200_OK)
        except:
            return Response(
                {"message": "School doesn't exist!"}, status=status.HTTP_404_NOT_FOUND
            )
    elif request.method == PUT:
        try:
            school = School.objects.get(school_id=school_ID)
            serializer = SchoolSerializer(school, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    elif request.method == DELETE:
        try:
            school = School.objects.get(school_id=school_ID)
            school.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response("School not found!", status=status.HTTP_404_NOT_FOUND)


@api_view([GET, PUT, DELETE])
def get_add_delete_teacher(request, school_ID: int):
    # ต้องแยกประเภทไหมว่าหาอะไรไม่เจอ
    if request.method == GET:
        try:
            school = School.objects.get(school_id=school_ID)
            teacher = Teacher.objects.filter(school_id=school)
            account = Account.objects.filter(account_id__in=teacher)
            result = JSONParser(account)
            return Response({"teachers": result})
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
    elif request.method == PUT:
        try:
            teachers = request.data["teachers"]
            tmpSchool = School.objects.get(school_id=school_ID)
            for i in teachers:
                tmpAcc = Account.objects.get(account_id=i)
                Teacher.objects.get_or_create(account_id=tmpAcc, school_id=tmpSchool)
            all_teachers = Teacher.objects.filter(school_id=school_ID)
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
                Teacher.objects.filter(account_id=i, school_id=school_ID).delete()
            all_teachers = Teacher.objects.filter(school_id=school_ID)
            result = JSONParser(all_teachers)  # แสดงผลครูทั้งหมดในโรงเรียน
            return Response({"teachers": result}, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view([GET])
def get_all_courses(request, school_id: int):
    try:
        school = School.objects.get(school_id=school_id)
    except School.DoesNotExist:
        return Response(
            {"message": "School doesn't not exists!"}, status=status.HTTP_404_NOT_FOUND
        )

    all_courses = Courses.objects.filter(school_id=school_id)
    serializer = CourseSerializer(all_courses, many=True)
    return Response(
        {"count": len(serializer.data), "result": serializer.data},
        status=status.HTTP_200_OK,
    )


@api_view([PUT])
def edit_status_school(request, school_ID: int):
    try:
        school = School.objects.get(school_id=school_ID)
        serializer = SchoolStatusSerializer(school, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

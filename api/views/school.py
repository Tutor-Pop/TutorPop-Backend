from cgitb import reset
from ..utility import JSONParser, JSONParserOne, passwordEncryption
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..constants.method import GET,POST,PUT,DELETE
from ..models import Account,PasswordHistory,School,Teacher

from cgitb import reset
from ..utility import JSONParser, JSONParserOne, passwordEncryption
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..constants.method import GET,POST,PUT,DELETE
from ..models import Account,PasswordHistory,School,Teacher
from rest_framework import status
from ..serializers import SchoolSerializer


@api_view([POST])
def create_school(request,id:int):
    account = Account.objects.get(account_id=id)
    school = School(
        owner = account,
        name = request.data['name'],
        description = request.data['description'],
        address = request.data['address'],
        status = request.data['status'],
        logo_url = request.data['logo_url'],
        banner_url = request.data['banner_url']
    )
    school.save()
    return Response({"message":"School created successfully","result":JSONParserOne(school)},status=status.HTTP_201_CREATED)

@api_view([GET,PUT,DELETE])
def get_edit_delete_school(request,school_ID:int):
    if request.method == GET:
        try:
            result = JSONParserOne(School.objects.get(school_id=school_ID))
            return Response({"data":result},status=status.HTTP_200_OK)
        except:
            return Response({"message":"School doesn't exist!"},state=status.HTTP_404_NOT_FOUND)
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

@api_view([GET,PUT,DELETE])
def get_add_delete_teacher(request,school_ID:int):
    #ต้องแยกประเภทไหมว่าหาอะไรไม่เจอ
    if request.method == GET:
        try:
            school = School.objects.get(school_id=school_ID)
            teacher = Teacher.objects.filter(school=school)
            account = Account.objects.filter(account_id__in=teacher)
            result = JSONParser(account)
            return Response({"data":result})
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
    elif request.method == PUT:
        try:
            teachers = request.data['teachers']
            for i in teachers:
                Teacher.objects.get_or_create(account_id=i, school_id=school_ID)
            all_teachers = Teacher.objects.filter(school_id=school_ID)
            result = JSONParser(all_teachers)       #แสดงผลครูทั้งหมดในโรงเรียน
            return Response({"teacher":result},status=status.HTTP_200_OK)
        except:
            # ถ้าใส่ "teachers":[1,5] จะเพิ่ม 1 แต่ไม่เพิ่ม 5
            return Response("Account or School Not Found",status=status.HTTP_404_NOT_FOUND)
    elif request.method == DELETE:
        try:
            teachers = request.data['teachers']
            for i in teachers:
                Teacher.objects.filter(account_id=i, school_id=school_ID).delete()
            all_teachers = Teacher.objects.filter(school_id=school_ID)
            result = JSONParser(all_teachers)       #แสดงผลครูทั้งหมดในโรงเรียน
            return Response({"teacher":result},status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

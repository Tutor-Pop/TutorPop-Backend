from ..utility import JSONParser, JSONParserOne
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..constants.method import GET,POST,PUT,DELETE
from ..models import Account,PasswordHistory, RoomUsage,School,Courses, SchoolRooms
from rest_framework import status
import django.db.utils

# @api_view([GET])
# def get_course(request,id:int):
#     yob = int(request.GET.get('year_of_birth',2000))
#     account = Account.objects.filter(is_deleted=False)
#     return Response(JSONParser(account))

@api_view([POST])
def create_course(request,school_id :int):
    school = School.objects.get(school_id=school_id)
    room = SchoolRooms.objects.get(room_id=request.data['room_id'])
    owner = Account.objects.get(account_id=request.data['owner_id'])
    course = Courses(
        school = school,
        owner = owner,
        course_name = request.data['course_name'],
        type = request.data['type'],
        course_description = request.data['course_description'],
        reserve_open_date = request.data['reserve_open_date'],
        reserve_close_date = request.data['reserve_close_date'],
        start_date = request.data['start_date'],
        end_date = request.data['end_date'],
        course_period = request.data['course_period'],
        course_price = request.data['course_price'],
        maximum_student = request.data['maximum_student'],
        reserved_student = 0,
        payment_method_text = request.data['payment_method_text'],
        payment_method_picture_url = request.data['payment_method_picture_url']
    )
    course.save()
    roomusage = RoomUsage(room=room,course=course)
    roomusage.save()
    return Response({"message":"Course created successfully","result":JSONParserOne(course)},status=status.HTTP_201_CREATED)

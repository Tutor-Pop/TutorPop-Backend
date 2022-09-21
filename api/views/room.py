from tkinter.font import ROMAN
from ..utility import JSONParser, JSONParserOne, passwordEncryption
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..constants.method import GET,POST,PUT,DELETE
from ..models import School,SchoolRooms
from rest_framework import status

@api_view([POST])
def create_room(request):
    pass

@api_view([GET,POST,PUT])
def get_create_update_room(request,school_id:int):
    try:
        school = School.objects.get(school_id=school_id)

        if request.method == GET:
            room = SchoolRooms.objects.filter(school_id=school)
            max_seat = request.GET.get("max_seat",-1)
            if max_seat != -1: room = room.filter(maximum_seat__lte=max_seat)
            return Response(JSONParser(room))

        room = SchoolRooms.objects.get(school_id=school,room_name=request.data['room_name'])
        
        if request.method == POST:
            return Response({"message":"Room already exists!"},status=status.HTTP_409_CONFLICT)

        elif request.method == PUT:  
            room.room_name = request.data['room_name']
            room.maximum_seat = request.data['maximum_seat']
            room.save()
            return Response(JSONParserOne(room),status=status.HTTP_200_OK)

    except SchoolRooms.DoesNotExist:

        if request.method == POST:
            room = SchoolRooms(
                school = school,
                room_name = request.data['room_name'],
                maximum_seat = request.data['maximum_seat']
            )
            room.save()
            return Response(JSONParserOne(room),status=status.HTTP_201_CREATED)

        return Response({"message": "Room doesn't not exists!"},status=status.HTTP_404_NOT_FOUND)
    except School.DoesNotExist:
        return Response({"message": "School doesn't not exists!"},status=status.HTTP_404_NOT_FOUND)

@api_view([GET])
def get_single_room(request,school_id:int,room_id:int):
    pass
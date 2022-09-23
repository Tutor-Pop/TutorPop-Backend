from tkinter.font import ROMAN
from ..utility import JSONParser, JSONParserOne, passwordEncryption
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..constants.method import GET,POST,PUT,DELETE
from ..models import School,SchoolRooms
from rest_framework import status

@api_view([POST])
def create_room(request,school_id:int):
    school = School.objects.get(school_id=school_id)
    # room = SchoolRooms.objects.get(school_id=school,room_name=request.data['room_name'])
    # return Response({"message":"Room already exists!"},status=status.HTTP_409_CONFLICT)
    room = SchoolRooms(
        school = school,
        room_name = request.data['room_name'],
        maximum_seat = request.data['maximum_seat']
    )
    room.save()
    return Response({'result':JSONParserOne(room)},status=status.HTTP_201_CREATED)
    

@api_view([GET,PUT,DELETE])
def get_update_room(request,school_id: int,room_id: int):
    try:
        school = School.objects.get(school_id=school_id)
        room = SchoolRooms.objects.get(school_id=school,room_id=room_id)

        if request.method == GET:
            pass
        
        elif request.method == PUT:  
            room.room_name = request.data['room_name']
            room.maximum_seat = request.data['maximum_seat']
            room.save()
            return Response({'result':JSONParserOne(room)},status=status.HTTP_200_OK)
        
        elif request.method == DELETE:
            room.is_deleted = True
            return Response(status=status.HTTP_204_OK)
        
        return Response({'result':JSONParserOne(room)},status=status.HTTP_200_OK)

    except SchoolRooms.DoesNotExist:
        return Response({"message": "Room doesn't not exists!"},status=status.HTTP_404_NOT_FOUND)
    except School.DoesNotExist:
        return Response({"message": "School doesn't not exists!"},status=status.HTTP_404_NOT_FOUND)

@api_view([GET])
def get_all_room_in_school(request,school_id:int):
    school = School.objects.get(school_id=school_id)
    room = SchoolRooms.objects.filter(school_id=school)
    max_seat = request.GET.get("max_seat",-1)
    if max_seat != -1: room = room.filter(maximum_seat__lte=max_seat)

    result = JSONParser(room)
    count = len(result)
    return Response({'count':count,'result':result},status=status.HTTP_200_OK)
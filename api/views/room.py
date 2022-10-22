from ..utility import JSONParser, JSONParserOne, passwordEncryption
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..constants.method import GET, POST, PUT, DELETE
from ..models import Courses, School, SchoolRooms
from rest_framework import status


@api_view([GET, POST, DELETE])
def create_getall_room(request, school_id: int):
    if request.method == GET:
        school = School.objects.get(school_id=school_id)
        room = SchoolRooms.objects.filter(school_id=school)
        max_seat = request.GET.get("max_seat", -1)
        if max_seat != -1:
            room = room.filter(maximum_seat__lte=max_seat)

        result = JSONParser(room)
        count = len(result)
        return Response({"count": count, "result": result}, status=status.HTTP_200_OK)
    elif request.method == POST:
        school = School.objects.get(school_id=school_id)
        # room = SchoolRooms.objects.get(school_id=school,room_name=request.data['room_name'])
        # return Response({"message":"Room already exists!"},status=status.HTTP_409_CONFLICT)
        room = SchoolRooms(
            school_id=school,
            room_name=request.data["room_name"],
            maximum_seat=request.data["maximum_seat"],
            description=request.data["description"],
        )
        room.save()
        return Response({"result": JSONParserOne(room)}, status=status.HTTP_201_CREATED)
    elif request.method == DELETE:
        try:
            school = School.objects.get(school_id=school_id)
        except School.DoesNotExist:
            return Response(
                {"message": "School does not exist"}, status=status.HTTP_404_NOT_FOUND
            )
        rooms_id = request.data["rooms_id"]
        ids = ""
        for room_id in rooms_id:
            try:
                room = SchoolRooms.objects.get(room_id=room_id)
            except SchoolRooms.DoesNotExist:
                ids += str(room_id)
                ids += ","
                continue
            room.delete()
        return Response(
            {"message": f"Deleted (except rooms with id {ids}. Rooms do not exist)"},
            status=status.HTTP_204_NO_CONTENT,
        )


@api_view([GET, PUT, DELETE])
def get_update_delete_room(request, school_id: int, room_id: int):
    try:
        school = School.objects.get(school_id=school_id)
        room = SchoolRooms.objects.get(school_id=school, room_id=room_id)

        if request.method == GET:
            pass

        elif request.method == PUT:
            room.room_name = request.data["room_name"]
            room.maximum_seat = request.data["maximum_seat"]
            room.description = request.data["description"]
            room.save()
            return Response({"result": JSONParserOne(room)}, status=status.HTTP_200_OK)

        elif request.method == DELETE:
            room.delete()
            # room.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response({"result": JSONParserOne(room)}, status=status.HTTP_200_OK)

    except SchoolRooms.DoesNotExist:
        return Response(
            {"message": "Room doesn't not exists!"}, status=status.HTTP_404_NOT_FOUND
        )
    except School.DoesNotExist:
        return Response(
            {"message": "School doesn't not exists!"}, status=status.HTTP_404_NOT_FOUND
        )


@api_view([GET])
def get_room_usage(request, room_id):
    course = Courses.objects.filter(roomusage__room_id=room_id).values(
        "course_id", "start_date", "end_date"
    )
    return Response({"usage": course}, status=status.HTTP_200_OK)

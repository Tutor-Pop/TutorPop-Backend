from cgitb import reset
from functools import partial
from importlib.abc import ResourceReader
from lib2to3.pgen2 import grammar
import stat
from ..serializers import ReservationSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..constants.method import GET, POST, PUT, DELETE
from ..models import OpenRequests, Reservation
from rest_framework import status
from ..filters import RequestFilter

# reservations/<id>


@api_view(['GET', 'DELETE'])
def get_del_reservation(request, resv_id: int):

    try:
        resv = Reservation.objects.get(id=resv_id)
    except Reservation.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = ReservationSerializer(resv)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        resv.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# reservations/
@api_view(['POST'])
def create_reservation(request):
    serializer = ReservationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# course/<course_id>/reservations


@api_view(['GET'])
def get_course_reservations(request, course_id: int):
    all_resv = Reservation.objects.filter(course=course_id)
    serializer = ReservationSerializer(all_resv, many=True)
    return Response({
        "count": len(serializer.data),
        "reservations": serializer.data
    }, status=status.HTTP_200_OK)

# reservations/<resv_id>/status


@api_view(['PUT'])
def update_reservation_status(request, resv_id: int):
    try:
        resv = Reservation.objects.get(id=resv_id)
    except Reservation.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = ReservationSerializer(resv, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

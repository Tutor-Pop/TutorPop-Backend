from ..serializers import ReservationSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from ..constants.method import GET, POST, PUT, DELETE
from ..models import OpenRequests, Reservation, Courses
from rest_framework import status
from ..filters import RequestFilter
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.utils import timezone
from datetime import timedelta, datetime


# reservations/<id>
@api_view(["GET", "DELETE"])
def get_del_reservation(request, resv_id: int):

    try:
        resv = Reservation.objects.get(id=resv_id)
    except Reservation.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        serializer = ReservationSerializer(resv)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "DELETE":
        resv.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# course/<course_id>/reservations


@api_view(["GET"])
def get_course_reservations(request, course_id: int):
    all_resv = Reservation.objects.filter(course_id=course_id, status="Confirmed")
    serializer = ReservationSerializer(all_resv, many=True)
    return Response(
        {"count": len(serializer.data), "reservations": serializer.data},
        status=status.HTTP_200_OK,
    )


# reservations/<resv_id>/status


@api_view(["PUT"])
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


class CreateReserve(APIView):
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def post(self, request, format=None):
        print(request.data)
        cid = request.data["course_id"]
        aid = request.data["account_id"]
        if Reservation.objects.get(course_id=cid, account_id=aid):
            return Response(
                {"message": "This account already reserved this course"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = ReservationSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            print("hi2")
            course_id = request.data["course_id"]
            course = Courses.objects.get(course_id=course_id)
            if course.reserved_student >= course.maximum_student:
                return Response(
                    {"message": "This course is full now."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            serializer.save()
            course.reserved_student += 1
            course.save()
            return Response(
                {"message": "Reservation Complete!", "Reservation": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UploadPayment(APIView):
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def put(self, request, resv_id: int, format=None):
        try:
            resv = Reservation.objects.get(id=resv_id)
        except Reservation.DoesNotExist:
            return Response(
                {"message": "Reservation not found"}, status=status.HTTP_404_NOT_FOUND
            )
        print(request.data)
        modified_data = request.data
        modified_data["status"] = "WaitForConfirm"
        serializer = ReservationSerializer(resv, data=modified_data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view([GET])
def get_revid(request, account_id: int, course_id: int):
    rev = Reservation.objects.get(account_id=account_id, course_id=course_id)
    revid = rev.id
    return Response({"reservation_id": revid}, status=status.HTTP_200_OK)

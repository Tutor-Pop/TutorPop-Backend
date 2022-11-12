from lib2to3.pgen2 import grammar
from lib2to3.pgen2.token import OP
from re import L
from ..serializers import RequestSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from ..constants.method import GET, POST, PUT, DELETE
from ..models import OpenRequests, School, Account
from rest_framework import status
from ..filters import RequestFilter
from api import serializers


##@api_view(['GET', 'POST'])
class get_create_request(APIView):
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def post(self, request):
        serializer = RequestSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"result": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        filterset = RequestFilter(
            request.GET,
            queryset=OpenRequests.objects.filter(request_status__icontains="Pending"),
        )
        if filterset.is_valid():
            queryset = filterset.qs
        serializer = RequestSerializer(queryset, many=True)
        reqs = serializer.data
        for req in reqs:
            sid = req["school_id"]
            aid = req["account_id"]
            sname = School.objects.get(school_id=sid).name
            oname = Account.objects.get(account_id=aid).username
            req["username"] = oname
            req["school_name"] = sname
        return Response(
            {"count": len(reqs), "requests": reqs},
            status=status.HTTP_200_OK,
        )


###class GetCreateRequest(APIView):
###    parser_classes = [MultiPartParser, FormParser]


@api_view(["GET", "DELETE", "PUT"])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def get_del_update_request(request, req_id: int):
    try:
        req = OpenRequests.objects.get(request_id=req_id)
    except OpenRequests.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        serializer = RequestSerializer(req)
        return Response({"result": serializer.data})
    elif request.method == "DELETE":
        req.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == "PUT":
        serializer = RequestSerializer(req, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"result": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
def update_request_status(request, req_id: int):
    try:
        req = OpenRequests.objects.get(request_id=req_id)
    except OpenRequests.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    req.request_status = request.data["status"]
    school = School.objects.get(school_id=req.school_id.school_id)
    school.status = request.data["status"]
    req.save()
    school.save()
    serializer = RequestSerializer(req)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["PUT"])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def upload_payment(request, req_id: int):
    try:
        req = OpenRequests.objects.get(request_id=req_id)
    except OpenRequests.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == "PUT":
        modified_data = request.data
        school = School.objects.get(school_id=req.school_id.school_id)
        modified_data["request_status"] = "PaymentPending"
        print(modified_data)
        serializer = RequestSerializer(req, data=modified_data, partial=True)
        if serializer.is_valid():
            serializer.save()
            school.status = "PaymentPending"
            school.save()
            return Response({"result": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view([GET])
def get_reqid_from_schoolid(request, school_id: int):
    req = OpenRequests.objects.get(school_id=school_id)
    reqid = req.request_id
    return Response({"request_id": reqid}, status=status.HTTP_200_OK)

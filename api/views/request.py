from lib2to3.pgen2 import grammar
from lib2to3.pgen2.token import OP
from re import L
from ..serializers import RequestSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..constants.method import GET, POST, PUT, DELETE
from ..models import OpenRequests
from rest_framework import status
from ..filters import RequestFilter
from api import serializers


@api_view(['GET', 'POST'])
def get_create_request(request):
    if request.method == 'POST':
        serializer = RequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        filterset = RequestFilter(
            request.GET, queryset=OpenRequests.objects.all())
        if filterset.is_valid():
            queryset = filterset.qs
        serializer = RequestSerializer(queryset, many=True)
        return Response(
            {"count": len(serializer.data),
             "requests": serializer.data},
            status=status.HTTP_200_OK)


@api_view(['GET', 'DELETE', 'PUT'])
def get_del_update_request(request, req_id: int):
    try:
        req = OpenRequests.objects.get(request_id=req_id)
    except OpenRequests.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = RequestSerializer(req)
        return Response(serializer.data)
    elif request.method == 'DELETE':
        req.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        serializer = RequestSerializer(req, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def update_request_status(request, req_id: int):
    try:
        req = OpenRequests.objects.get(request_id=req_id)
    except OpenRequests.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    req.request_status = request.data['status']
    req.save()
    serializer = RequestSerializer(req)
    return Response(serializer.data)

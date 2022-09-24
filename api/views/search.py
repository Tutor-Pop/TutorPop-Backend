from datetime import datetime, date
from re import search
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..constants.method import GET, POST, PUT, DELETE
from ..models import Courses, School
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..serializers import CourseSerializer, SchoolSerializer


class api_course_search(ListAPIView):
    serializer_class = CourseSerializer
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    search_fields = ('course_name', 'course_description', 'school__name')

    def get_queryset(self):
        queryset = Courses.objects.all()
        min_price = self.request.query_params.get('min_price', 0)
        max_price = self.request.query_params.get('max_price', 1000000000)
        type = self.request.query_params.get('type', '')
        is_deleted = self.request.query_params.get('is_deleted', False)
        max_student = self.request.query_params.get('max_student', '')
        start_date = self.request.query_params.get(
            'start_date', date.today())
        end_date = self.request.query_params.get('end_date', '')
        queryset = queryset.filter(
            course_price__gte=min_price, course_price__lte=max_price,
            is_deleted=is_deleted,
            start_date__gte=start_date,
        )
        if type:
            queryset = queryset.filter(type=type)
        if max_student:
            queryset = queryset.filter(maximum_student__lte=max_student)
        if end_date:
            queryset = queryset.filter(end_date__lte=end_date)
        return queryset

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data = {'count': len(response.data), 'result': response.data}
        return response


class api_school_search(ListAPIView):
    serializer_class = SchoolSerializer
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    search_fields = ('name', 'description')

    def get_queryset(self):
        queryset = School.objects.all()
        status = self.request.query_params.get('status', 'OPEN')
        address = self.request.query_params.get('address', '')
        queryset = queryset.filter(status=status)
        if address:
            queryset = queryset.filter(address=address)
        return queryset

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data = {'count': len(response.data), 'result': response.data}
        return response

from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..constants.method import GET, POST, PUT, DELETE
from ..models import Courses, School
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..serializers import CourseSerializer


class api_course_search(ListAPIView):
    queryset = Courses.objects.all()
    serializer_class = CourseSerializer
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    search_fields = ('course_name',
                     'course_description', 'school__name')
    filter_fields = ('type', 'course_id', 'school_id',)

    def get_queryset(self):
        queryset = Courses.objects.all()
        min_price = self.request.query_params.get('min_price', '0')
        max_price = self.request.query_params.get('max_price', '10000000')

        if (min_price and max_price):
            queryset = queryset.filter(course_price__gt=min_price,
                                       course_price__lt=max_price)
        return queryset

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data = {'count': len(response.data),
                         'result': response.data}
        return response

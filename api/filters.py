import django_filters
from .models import OpenRequests


class RequestFilter(django_filters.FilterSet):
    class Meta:
        model = OpenRequests
        fields = ['request_id', 'account_id', 'school_id', 'request_status']

from doctest import REPORT_UDIFF
from ..utility import JSONParser, JSONParserOne, passwordEncryption
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..constants.method import GET, POST, PUT, DELETE
from ..models import Courses, School, Account, OpenRequests
from rest_framework import status
from django.db.models import Q
from django.utils import timezone

# Item.objects.filter(Q(creator=owner) | Q(moderated=False)
@api_view([GET])
def get_active_stat(request):
    accs = Account.objects.count()
    crs = Courses.objects.filter(is_deleted=False).count()
    scs = School.objects.filter(status="OPEN").count()
    return Response(
        {"accounts": accs, "courses": crs, "schools": scs}, status=status.HTTP_200_OK
    )


@api_view([GET])
def get_pending_request(request):
    reqs = OpenRequests.objects.filter(request_status__contains="Pending").count()

    return Response({"pending_req": reqs}, status=status.HTTP_200_OK)


@api_view([GET])
def get_month_stat(request):
    today = timezone.now().date()
    current_month = today.month
    current_year = today.year
    acc = Account.objects.filter(
        created_date__month=current_month, created_date__year=current_year
    ).count()
    scc = School.objects.filter(
        openrequests__request_timestamp__month=current_month,
        openrequests__request_timestamp__year=current_year,
        status="OPEN",
    ).count()
    crs = Courses.objects.filter(
        reserve_open_date__month=current_month,
        reserve_open_date__year=current_year,
        is_deleted=False,
    ).count()
    return Response(
        {"tm_accounts": acc, "tm_courses": crs, "tm_schools": scc},
        status=status.HTTP_200_OK,
    )

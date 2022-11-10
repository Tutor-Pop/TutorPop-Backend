from doctest import REPORT_UDIFF
from ..utility import JSONParser, JSONParserOne, passwordEncryption
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..constants.method import GET, POST, PUT, DELETE
from ..models import Courses, School, Account, OpenRequests
from rest_framework import status
from django.db.models import Q

# Item.objects.filter(Q(creator=owner) | Q(moderated=False)
@api_view([GET])
def get_active_stat(request):
    accs = School.objects.count()
    crs = Courses.objects.filter(is_deleted=False).count()
    scs = School.objects.filter(status="OPEN").count()
    return Response(
        {"accounts": accs, "Courses": crs, "Schools": scs}, status=status.HTTP_200_OK
    )


@api_view([GET])
def get_pending_request(request):
    reqs = OpenRequests.objects.filter(request_status__contains="Pending").count()

    return Response({"pending_req": reqs}, status=status.HTTP_200_OK)

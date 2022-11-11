from cgitb import reset
from ..utility import JSONParser, JSONParserOne, passwordEncryption
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..constants.method import GET, POST
from ..models import Account, Notification
from rest_framework import status
import datetime
from django.utils import timezone


@api_view([POST])
def create_notification(request):
    account = Account.objects.get(account_id=request.data["account_id"])
    notification = Notification(
        account_id=account,
        title=request.data["title"],
        message_noti=request.data["message_noti"],
        create_time=timezone.now(),
        expire_date=request.data["expire_date"],
    )
    notification.save()
    result = JSONParserOne(notification)
    return Response({"message": result}, status=status.HTTP_200_OK)


@api_view([GET])
def get_all_notification(request, account_id: int):
    now = timezone.now()
    notificationData = JSONParser(Notification.objects.filter(account_id=account_id))
    count = len(notificationData)
    countDict = {"count": count}
    return Response(
        {"count": countDict["count"], "messages": notificationData},
        status=status.HTTP_200_OK,
    )


@api_view([GET])
def get_notexpire_notification(request, account_ID: int):
    # print(type(current.date()))
    # print(datetime.date.today())
    notificationData = JSONParser(
        Notification.objects.filter(
            account_id=account_ID, expire_date__gte=timezone.now().date()
        )
    )
    count = len(notificationData)
    countDict = {"count": count}
    return Response(
        {"count": countDict["count"], "messages": notificationData},
        status=status.HTTP_200_OK,
    )

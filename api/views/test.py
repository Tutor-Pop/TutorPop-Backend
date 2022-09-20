from ..utility import JSONParser, JSONParserOne, passwordEncryption
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..constants.method import GET,POST,PUT,DELETE
from ..models import Account,PasswordHistory,School
import django.db.utils

@api_view([GET])
def get_acounts(request):
    yob = int(request.GET.get('year_of_birth',2000))
    account = Account.objects.filter(is_deleted=False)
    return Response(JSONParser(account))

@api_view([PUT])
def edit_account(request,id:int):
    account = Account.objects.get(account_id=id)
    account.firstname = "AAAAAAAAAAA"
    account.save()
    return Response("Edit sucess")

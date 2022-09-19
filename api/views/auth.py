from ..utility import JSONParser, JSONParserOne, passwordEncryption
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..constants.method import GET,POST,PUT,DELETE
from ..models import Account,PasswordHistory,School
import django.db.utils

@api_view([POST])
def register(request):
    try:
        ePassword = passwordEncryption(request.POST.get('password',""))
        account = Account(
            firstname = request.POST.get('firstname',""),
            lastname = request.POST.get('lastname',""),
            username = request.POST.get('username',""),
            password = ePassword,
            email = request.POST.get('email',""),
            year_of_birth = request.POST.get('year_of_birth',""),
            description = request.POST.get('description',""),
            is_verified = False,
            profile_picture = "",
            is_deleted = False
        )
        account.save()
        passwordHistory = PasswordHistory(
            account = account,
            password = ePassword
        )
        passwordHistory.save()
        return Response("Registration Completed!")
    except django.db.utils.IntegrityError:
        return Response("Email/Username already existed!")
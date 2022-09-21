from ..utility import JSONParser, JSONParserOne, passwordEncryption
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..constants.method import GET,POST,PUT,DELETE
from ..models import Account,PasswordHistory,School
import django.db.utils

@api_view([POST])
def register(request):
    try:
        ePassword = passwordEncryption(request.data['password'])
        print(request.POST.get('username',"No Name"))
        account = Account(
            firstname = request.data["firstname"],
            lastname = request.data["lastname"],
            username = request.data["username"],
            password = ePassword,
            email = request.data["email"],
            year_of_birth = request.data["year_of_birth"],
            description = request.data["description"],
            profile_picture = "",
            is_verified = False,
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
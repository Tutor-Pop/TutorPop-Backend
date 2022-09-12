from ast import Pass
from base64 import encode
from ..constants.utility import JSONParser, JSONParserOne
from rest_framework.response import Response
from rest_framework.decorators import api_view
import hashlib
from ..constants.method import GET,POST,PUT,DELETE
from ..models import Account,PasswordHistory,School
import django.db.utils

@api_view([POST])
def register(request):
    try:
        account = Account(
            firstname=request.data['firstname'],
            lastname=request.data['lastname'],
            username=request.data['username'],
            password=request.data['password'],
            email=request.data['email'],
            year_of_birth=request.data['year_of_birth'],
            description=request.data['description'],
            is_verified=request.data['is_verified'],
            profile_picture=request.data['profile_picture'],
            user_status=request.data['user_status']
        )
        account.save()
        passwordHistory = PasswordHistory(
            account_id = account,
            password = request.data['password']
        )
        passwordHistory.save()
        return Response("Registration Completed!")
    except django.db.utils.IntegrityError:
        return Response("Email/Username already existed!")

@api_view([GET])
def get_all_accounts(request):
    result = JSONParser(Account.objects.all())
    return Response({"count":len(result),"data":result})

@api_view([GET])
def get_account(request,id:int):
    try:
        result = JSONParserOne(Account.objects.get(account_id=id))
        return Response({"data":result})
    except Account.DoesNotExist:
        return Response({"message":"Account doesn't exist!"})

@api_view([PUT])
def change_password(request,id:int):
    account = Account.objects.get(account_id=id)
    account.password = request.data['password']
    account.save()
    passwordHistory = PasswordHistory(account_id=account,password=request.data['password'])
    passwordHistory.save()
    return Response({"message": f"{account.username} password has been changed!"})

@api_view([POST])
def create_school(request,id:int):
    account = Account.objects.filter(account_id=id)
    school = School(
        name = request.data['name'],
        description = request.data['description'],
        address = request.data['address'],
        status = request.data['status'],
        logo_url = request.data['logo_url'],
        banner_url = request.data['banner_url']
    )
    school.save()
    school.owner_id.set(account)
    return Response("School created successfully")
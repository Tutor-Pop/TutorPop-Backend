from django.forms import model_to_dict
from ..utility import JSONParser, JSONParserOne, passwordEncryption
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from ..constants.method import GET,POST,PUT,DELETE
from ..models import Account,PasswordHistory,School
import django.db.utils
from uuid import uuid4
from time import time

TOKEN_LIFETIME = 30*60 # (Second)

@api_view([POST])
def login(request):
    try:
        account = Account.objects.get(username=request.data['username'])
        account_dict = model_to_dict(account)

        if passwordEncryption(request.data['password']) == account_dict['password']:
            account.token = uuid4().hex
            account.token_expire = int(time()+TOKEN_LIFETIME)
            account.save()
            return Response(model_to_dict(account),status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'detail':"Incorrect password!"},status=status.HTTP_406_NOT_ACCEPTABLE)
    except Account.DoesNotExist:
        return Response({'detail':"User doesn't exists!"},status=status.HTTP_404_NOT_FOUND)

@api_view([POST])
def logout(request):
    try:
        account = Account.objects.get(account_id=request.data['account_id'])
        if account.token == request.data['token']:
            account.token = None
            account.save()
            return Response(model_to_dict(account),status=status.HTTP_200_OK)
        else:
            return Response({'detail':"Invalid token!"},status=status.HTTP_200_OK)
    except Account.DoesNotExist:
        return Response({'detail':"User doesn't exists!"},status=status.HTTP_404_NOT_FOUND)

@api_view([PUT])
def get_authorization(request):
    try:
        account = Account.objects.get(account_id=request.data['account_id'])
        account_dict = model_to_dict(account)
        if account_dict['token_expire'] >= time() and account_dict['token'] == request.data['token']:
            return Response({'result':True},status=status.HTTP_200_OK)
        return Response({'result':False},status=status.HTTP_200_OK)
    except Account.DoesNotExist:
        return Response({'result':False},status=status.HTTP_200_OK)

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
            account_id = account,
            password = ePassword
        )
        passwordHistory.save()
        return Response({'message':"Registration Completed!",'result':JSONParserOne(account)})
    except django.db.utils.IntegrityError:
        return Response({'message':"Email/Username already existed!",'result': {}})
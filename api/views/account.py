from xmlrpc.client import Boolean
from ..utility import JSONParser, JSONParserOne, passwordEncryption
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..constants.method import GET,POST,PUT,DELETE
from ..models import Account,PasswordHistory,School
from rest_framework import status

@api_view([GET])
def get_all_accounts(request):
    
    offset = int(request.GET.get('offset',0))
    limit = int(request.GET.get('limit',-1))
    user_id = int(request.GET.get('user_id',0))
    is_verified = request.GET.get('is_verified',1) == 1
    year_of_birth = int(request.GET.get('year_of_birth',0))

    print(is_verified)

    result = JSONParser(Account.objects.filter(
        is_deleted=False,
        # account_id=user_id,
        is_verified=is_verified,
        # year_of_birth=year_of_birth
    ).order_by("account_id"))

    if limit == -1:
        limit = len(result)
    #--- Lowerbound cannot be greater than Upperbound ---#
    if offset > limit:
        return Response({"message":"Offset value cannot be greater than limit value"})
    

    
    total = limit - offset

    return Response({"offset":offset,"limit":limit,"count":total,"data":result[offset:limit]})

@api_view([GET,PUT,DELETE])
def get_edit_delete_account(request,id:int):
    if request.method == GET:
        try:
            result = JSONParserOne(Account.objects.get(account_id=id))
            return Response({"data":result})
        except Account.DoesNotExist:
            return Response({"message":"Account doesn't exist!"},status=status.HTTP_404_NOT_FOUND)
    elif request.method == PUT:
        try:
            account = Account.objects.get(account_id=id)
            for data in request.data:
                if hasattr(account,data):
                    setattr(account,data,request.data[data])
            account.save()
            return Response({"data": JSONParserOne(account)})
        except:
            pass
    elif request.method == DELETE:
        try:
            account = Account.objects.get(account_id=id)
            account.is_deleted = True
            account.save()
            return Response(f"{account.username} has been deleted!")
        except:
            return Response("Account not found!")

@api_view([PUT])
def change_password(request,id:int):
    if passwordEncryption(request.data['password']) in [i.password for i in PasswordHistory.objects.filter(account_id=id)]:
        return Response("Try another password!")
    account = Account.objects.get(account_id=id)
    account.password = passwordEncryption(request.data['password'])
    account.save()
    passwordHistory = PasswordHistory(account_id=account,password=passwordEncryption(request.data['password']))
    passwordHistory.save()
    return Response({"message": f"{account.username} password has been changed!"})

@api_view([POST])
def create_school(request,id:int):
    account = Account.objects.get(account_id=id)
    school = School(
        owner = account,
        name = request.data['name'],
        description = request.data['description'],
        address = request.data['address'],
        status = request.data['status'],
        logo_url = request.data['logo_url'],
        banner_url = request.data['banner_url']
    )
    school.save()
    return Response("School created successfully")



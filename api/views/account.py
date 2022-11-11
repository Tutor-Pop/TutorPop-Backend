from ..utility import JSONParser, JSONParserOne, passwordEncryption
from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes
from ..constants.method import GET, POST, PUT, DELETE
from ..models import Account, PasswordHistory, School
from rest_framework import status
from ..serializers import AccountSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.parsers import JSONParser as JP


@api_view([GET])
def get_all_accounts(request):

    offset = int(request.GET.get("offset", 0))
    limit = int(request.GET.get("limit", -1))
    account_id = int(request.GET.get("account_id", -1))
    is_verified = int(request.GET.get("is_verified", 1)) == 1
    year_of_birth = int(request.GET.get("year_of_birth", -1))

    print("Query", offset, limit, account_id, is_verified, year_of_birth)

    account = Account.objects.filter(is_deleted=False, is_verified=is_verified)

    if account_id != -1:
        account = account.filter(account_id=account_id)
    if year_of_birth != -1:
        account = account.filter(year_of_birth=year_of_birth)
    if limit == -1:
        limit = len(account)
    if offset > limit:
        return Response(
            {"message": "Offset value cannot be greater than limit value"},
            status=status.HTTP_406_NOT_ACCEPTABLE,
        )

    total = limit - offset
    result = JSONParser(account.order_by("account_id"))
    return Response(
        {
            "offset": offset,
            "limit": limit,
            "count": total,
            "result": result[offset:limit],
        },
        status=status.HTTP_200_OK,
    )


@api_view([GET, PUT, DELETE])
@parser_classes([MultiPartParser, FormParser, JP])
def get_edit_delete_account(request, id: int):
    if request.method == GET:
        try:
            result = JSONParserOne(Account.objects.get(account_id=id))
            return Response({"result": result})
        except Account.DoesNotExist:
            return Response(
                {"message": "Account doesn't exist!"}, status=status.HTTP_404_NOT_FOUND
            )
    elif request.method == PUT:
        try:
            account = Account.objects.get(account_id=id)
            serializer = AccountSerializer(account, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"message": "update successfully", "account": serializer.data},
                    status=status.HTTP_200_OK,
                )
        except Exception as e:
            return Response({"message": e}, status=status.HTTP_406_NOT_ACCEPTABLE)
        except Account.DoesNotExist:
            return Response(
                {"message": "Account does not exist."}, status=status.HTTP_200_OK
            )
    elif request.method == DELETE:
        try:
            account = Account.objects.get(account_id=id)
            account.is_deleted = True
            account.save()
            return Response(
                {"result": JSONParserOne(account)}, status=status.HTTP_200_OK
            )
        except:
            return Response(
                {"message": "Account not found!"}, status=status.HTTP_404_NOT_FOUND
            )


@api_view([PUT])
def change_password(request, id: int):
    if passwordEncryption(request.data["password"]) in [
        i.password for i in PasswordHistory.objects.filter(account_id=id)
    ]:
        return Response(
            {"message": "Try another password!"}, status=status.HTTP_406_NOT_ACCEPTABLE
        )
    account = Account.objects.get(account_id=id)
    account.password = passwordEncryption(request.data["password"])
    account.save()
    passwordHistory = PasswordHistory(
        account_id=account, password=passwordEncryption(request.data["password"])
    )
    passwordHistory.save()
    return Response(
        {"result": JSONParserOne(passwordHistory)}, status=status.HTTP_200_OK
    )

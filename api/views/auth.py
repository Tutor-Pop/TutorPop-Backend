from django.forms import model_to_dict
from ..utility import JSONParser, JSONParserOne, passwordEncryption
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from ..constants.method import GET, POST, PUT, DELETE
from ..models import Account, PasswordHistory, School
import django.db.utils
from uuid import uuid4
from time import time
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect
from ..tokens import account_activation_token
from ..serializers import AccountSerializer

TOKEN_LIFETIME = 30 * 60  # (Second)


def activateEmail(request, user, to_email):
    mail_subject = "Activate your user account."
    message = render_to_string(
        "template_activate_email.html",
        {
            "user": user.username,
            "domain": get_current_site(request).domain,
            "uid": urlsafe_base64_encode(force_bytes(user.account_id)),
            "token": account_activation_token.make_token(user),
            "protocol": "https" if request.is_secure() else "http",
        },
    )
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        return True


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Account.objects.get(account_id=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_verified = True
        user.save()
        return HttpResponseRedirect(redirect_to="https://google.com")
    return HttpResponseRedirect(redirect_to="https://google.com")


@api_view([POST])
def login(request):
    try:
        account = Account.objects.get(username=request.data["username"])
        account_dict = model_to_dict(account)

        if passwordEncryption(request.data["password"]) == account_dict["password"]:
            # print("hi")
            account.token = uuid4().hex
            account.token_expire = int(time() + TOKEN_LIFETIME)
            account.save()
            serializer = AccountSerializer(account)
            # print("hi")
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(
                {"detail": "Incorrect password!"}, status=status.HTTP_406_NOT_ACCEPTABLE
            )
    except Account.DoesNotExist:
        return Response(
            {"detail": "User doesn't exists!"}, status=status.HTTP_404_NOT_FOUND
        )


@api_view([POST])
def logout(request):
    try:
        account = Account.objects.get(account_id=request.data["account_id"])
        if account.token == request.data["token"]:
            account.token = None
            account.save()
            return Response(model_to_dict(account), status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Invalid token!"}, status=status.HTTP_200_OK)
    except Account.DoesNotExist:
        return Response(
            {"detail": "User doesn't exists!"}, status=status.HTTP_404_NOT_FOUND
        )


@api_view([PUT])
def get_authorization(request):
    try:
        account = Account.objects.get(account_id=request.data["account_id"])
        account_dict = model_to_dict(account)
        if (
            account_dict["token_expire"] >= time()
            and account_dict["token"] == request.data["token"]
        ):
            return Response({"result": True}, status=status.HTTP_200_OK)
        return Response({"result": False}, status=status.HTTP_200_OK)
    except Account.DoesNotExist:
        return Response({"result": False}, status=status.HTTP_200_OK)


@api_view([POST])
def register(request):
    try:
        ePassword = passwordEncryption(request.data["password"])
        print(request.POST.get("username", "No Name"))
        account = Account(
            firstname=request.data["firstname"],
            lastname=request.data["lastname"],
            username=request.data["username"],
            password=ePassword,
            email=request.data["email"],
            year_of_birth=request.data["year_of_birth"],
            description=request.data["description"],
            profile_picture=None,
            is_verified=False,
            is_deleted=False,
        )
        account.save()
        # print("hi")
        passwordHistory = PasswordHistory(account_id=account, password=ePassword)
        passwordHistory.save()
        if not activateEmail(request, account, account.email):
            account.delete()
            return Response(
                {"message": "Send mail failed"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        # print("hi2")
        serializer = AccountSerializer(account)
        return Response(
            {"message": "Registration Completed!", "result": serializer.data}
        )
    except django.db.utils.IntegrityError:
        return Response({"message": "Email/Username already existed!", "result": {}})

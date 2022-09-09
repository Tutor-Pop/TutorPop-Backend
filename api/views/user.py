from base64 import encode
from rest_framework.response import Response
from rest_framework.decorators import api_view
import hashlib
from ..constants.method import GET,POST,PUT,DELETE
from ..models import User

@api_view([POST])
def register(request):
    account = User(
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
    print(account)
    return Response("OK")
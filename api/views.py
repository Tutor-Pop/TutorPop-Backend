from base64 import encode
from rest_framework.response import Response
from rest_framework.decorators import api_view
import hashlib
from .constants.method import GET,POST,PUT,DELETE

account = {}
cookie = {}
sample_data = []

def passwordEncryption(password):
    print(password)
    hash = hashlib.sha512(password.encode('utf-8')) #ข้อความที่จะแฮชคือ 1111
    return hash.hexdigest()

@api_view([GET])
def getData(request):
    sample_data.append(1)
    return Response(sample_data)

@api_view([GET,POST])
def registerAccount(request):
    if request.method == GET:
        return Response({
        "count": len(account),
        "account": account
    })
    elif request.method == POST:
        new_account = request.data
        print("AAAAAAAAAAAAAAAAAAA",new_account)
        if new_account['username'] in [i['username'] for i in account]:
            return Response({"message": "User already existed!"})
        new_account['data'] = []
        new_account['password'] = passwordEncryption(new_account['password'])
        account[new_account['username']] = new_account
        return Response(new_account)

@api_view([POST])
def loginAccount(request):
    login = request.data
    login['password'] = passwordEncryption(login['password'])
    if request.method == POST:
        if login['username'] in account:
            if login['password'] == account[login['username']]['password']:
                return Response({"message": "Login successful"})
            else:
                return Response({"message": "Wrong password"})
        else:
            return Response({"message": "This user doesn't exist!"})

@api_view([GET,PUT])
def personalAccount(request,username=None):
    if request.method == GET:
        try:
            return Response([i for i in account if i['username'] == username][0])
        except:
            return Response("No")
    if request.method == PUT:
        try:
            target = [i for i in account if i['username'] == username][0]
            target['data'].append(request.query_params['sample'])
            return Response(target)
        except:
            return Response("No")



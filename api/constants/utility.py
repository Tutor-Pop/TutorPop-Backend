from hashlib import sha512

def JSONParser(class_object):
    return [{j:vars(i)[j] for j in vars(i) if j != '_state'} for i in class_object]

def JSONParserOne(class_object):
    class_dict = vars(class_object)
    return {i:class_dict[i] for i in class_dict if i != '_state'}

def passwordEncryption(password):
    ePassword = sha512(str(password).encode('utf8'))
    return ePassword.hexdigest()
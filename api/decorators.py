# coding=utf8
# -*- coding: utf8 -*-
# vim: set fileencoding=utf8 :

from django.http import HttpResponse
from functools import wraps

# modelo sem parametro
def login_required_and_notify(my_function):  # @login_required_and_notify
    def wrapper(*args, **kwargs):
        return my_function(*args, **kwargs)
    return wrapper

# modelo com parametro
def check_referrer(path): # @check_referrer('teste')
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            return f(*args, **kwargs)

        return decorated

    return decorator


def is_auth(func):  # @login_required_and_notify
    def wrapper(request, *args, **kwargs):
        if request.META.get('HTTP_AUTHORIZATION') != None:
            token = request.META.get('HTTP_AUTHORIZATION')
            token_decode = jwt.decode(token, 'secret', algorithms=['HS256'])
            # token_serializer =  serializers.serialize("json", token_decode)
            for key, value in token_decode.items():
                username = key
                password = value

            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    return func(*args, **kwargs)
                else:
                    return HttpResponse('404') #usuario desativado

            else:
                return HttpResponse('400') #usuario ou senha incorreta
        else:
            return HttpResponse('401') #nao autorizado
    return wrapper

# def is_auth(view_func):
#     def _decorator(request, *args, **kwargs):
#         if request.META.get('HTTP_AUTHORIZATION') != None:
#             token = request.META.get('HTTP_AUTHORIZATION')
#             token_decode = jwt.decode(token, 'secret', algorithms=['HS256'])
#             # token_serializer =  serializers.serialize("json", token_decode)
#             for key, value in token_decode.items():
#                 username = key
#                 password = value

#             user = authenticate(username=username, password=password)
#             request.user.username = username
#             request.user.password = password
#             # return HttpResponse(username)
#             return func()
#         else:
#             return HttpResponse('401') #nao autorizado
            
#     return _decorator

# def teste(myfunc):
#     def _decorator(request):
#         if request.META.get('HTTP_AUTHORIZATION') != None:
#             token = request.META.get('HTTP_AUTHORIZATION')
#             token_decode = jwt.decode(token, 'secret', algorithms=['HS256'])
#             # token_serializer =  serializers.serialize("json", token_decode)
#             for key, value in token_decode.items():
#                 username = key
#                 password = value

#             user = authenticate(username=username, password=password)
#             if user:
#                 if user.is_active:
#                     return myfunc('ok')
#                 else:
#                     return HttpResponse('404') #usuario desativado

#             else:
#                 return HttpResponse('400') #usuario ou senha incorreta
#         else:
#             return HttpResponse('401') #nao autorizado
            
#     return _decorator
import jwt
from django.core import serializers
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User, Permission, Group
from django.contrib.auth import authenticate, login as auth_login, logout
from api.forms import *
from api.models import *

def error_form_serialization(error_dict):  
    """  
    This method strips the proxy objects from the
    error dict and casts them to unicode. After
    that the error dict can and will be
    json-serialized.  
    """  
    plain_dict = dict([(k, [unicode(e) for e in v]) for k,v in error_dict.items()])   
    return simplejson.dumps(plain_dict)

@csrf_exempt
def index(request):
    return HttpResponse("e-pedidos")

@csrf_exempt
def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                token = jwt.encode({request.POST.get('username',False): request.POST.get('password',False)}, 'secret', algorithm='HS256')                
                return HttpResponse('{"token":"'+token+'"}')
            else:
                return HttpResponse('404') #usuario desativado

        else:
            return HttpResponse('400') #usuario ou senha incorreta

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        register_form = RegisterForm(data=request.POST)
        if register_form.is_valid():
            try:
                register = register_form.save()
                register.set_password(register.password)
                register.save()
                token = jwt.encode({request.POST.get('username',False): request.POST.get('password',False)}, 'secret', algorithm='HS256')
                return HttpResponse('{"token":"'+token+'"}')
            except:
                return HttpResponse('500')
        else:
            return HttpResponse(error_form_serialization(register_form.errors))

def cliente(request):
    user = User.objects.get(pk=request.user.pk)
    user_profile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        cliente_form = ClienteForm(data=request.POST)
        if cliente_form.is_valid():
            cliente = cliente_form.save(commit=False)
            cliente.usuario_criacao = user
            cliente.usuario_modificacao = user
            cliente.conta_sistema = user_profile.conta_sistema
            cliente.save()
            return HttpResponse(200)
        else:
            return HttpResponse(error_form_serialization(cliente_form.errors))
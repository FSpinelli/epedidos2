# coding=utf8
# -*- coding: utf8 -*-
# vim: set fileencoding=utf8 :

import jwt
from django.core import serializers
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User, Permission, Group
from django.contrib.auth import authenticate, login as auth_login, logout
from api.forms import *
from api.models import *

@csrf_exempt
def index(request):
    return HttpResponse("epedidos api")

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        register_form = RegisterForm(data=request.POST)
        if register_form.is_valid():
            try:
                register = register_form.save()
                register.set_password(register.password)
                register.save()
                user = User.objects.filter(pk=register.pk)
                user_serializer = serializers.serialize("json", user)
                a = AccountSystem()
                a.name = request.POST.get('name',False)
                a.save()
                user_profile = UserProfile()
                user_profile.user = User.objects.get(pk=register.pk)
                user_profile.account_system = a
                user_profile.save()
                return HttpResponse('201')
            except:
                return HttpResponse('500')
        else:
            return HttpResponse(register_form.errors)

@csrf_exempt
def signin(request):
    if request.method == 'GET':
        username = request.GET['username']
        password = request.GET['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                token = jwt.encode({request.GET.get('username',False): request.GET.get('password',False)}, 'secret', algorithm='HS256')

                user = User.objects.filter(pk=user.pk)
                user_profile = UserProfile.objects.filter(user=user)
                user_profile.update(access_token=token)
                
                user_serializer = serializers.serialize("json", user)
                userprofile_serializer = serializers.serialize("json", user_profile)
                return HttpResponse('[{"user":"'+user_serializer+'", "user_profile":"'+userprofile_serializer+'"}]')
            else:
                return HttpResponse("{'mensagem':'Seu usuário está desativado.'}")

        else:
            return HttpResponse("{'mensagem':'Usuário ou senha incorreta.'}")

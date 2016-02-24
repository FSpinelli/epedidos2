# coding=utf8
# -*- coding: utf8 -*-
# vim: set fileencoding=utf8 :

from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from .forms import *
from api.models import *

@csrf_exempt
def cadastrar(request):
    if request.method == 'POST':
        conta_sistema_form = ContaSistemaForm(data=request.POST)
        cadastro_form = CadastroForm(data=request.POST)
        if cadastro_form.is_valid():
            cadastro = cadastro_form.save()
            cadastro.set_password(cadastro.password)
            cadastro.save()
            user = User.objects.get(pk=cadastro.pk)
            conta_sistema = ContaSistema()
            conta_sistema.nome = request.POST['nome']
            conta_sistema.usuario_criacao=user
            conta_sistema.usuario_modificacao=user
            conta_sistema.save()
            user_profile = UserProfile(conta_sistema=conta_sistema, user=user).save()
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            auth_login(request, user)
            return HttpResponseRedirect('/')
        else:
            print cadastro_form.errors
    else:
        cadastro_form = CadastroForm()
        conta_sistema_form = ContaSistemaForm()
    return render(
    		request,
            'app/cadastrar.html',
            {'cadastro_form': cadastro_form, 'conta_sistema_form': conta_sistema_form})

@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                auth_login(request, user)
                if request.session['pag_login_required'] == "":
                    return HttpResponseRedirect('/')
                else:
                    return HttpResponseRedirect(request.session['pag_login_required'])
            else:
                context = {'mensagem':'Seu usuário está desativado.'}
        else:
            context = {'mensagem':'Usuário ou senha incorreta.'}
    else:
        context = {}
        if request.GET.get('next'):
            request.session['pag_login_required'] = request.GET['next']
        else:
            request.session['pag_login_required'] = ""
    return render(request, 'app/login.html', context)

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/login/')

@login_required
def index(request):
    user = User.objects.get(pk=request.user.pk)
    return render(request, 'app/index.html', {'user':user})
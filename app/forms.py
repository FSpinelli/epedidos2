 	# coding=utf8
# -*- coding: utf8 -*-
# vim: set fileencoding=utf8 :

from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from django import forms
from api.models import *

class CadastroForm(forms.ModelForm):
    username = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control', 'type': 'email', 'placeholder':'E-mail'}))
    password = forms.CharField(widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'Senha'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'required': 'true', 'placeholder':'Nome'}))
    last_name = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control', 'required': 'true', 'placeholder':'Sobrenome'}))

    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'last_name')

class ContaSistemaForm(forms.ModelForm):
	nome = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Empresa'}))
	
	class Meta:
		model = ContaSistema
		exclude = ('usuario_criacao', 'usuario_modificacao')
        fields = ('nome')
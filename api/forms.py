# coding=utf8
# -*- coding: utf8 -*-
# vim: set fileencoding=utf8 :

from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from django import forms
from api.models import *

class RegisterForm(forms.ModelForm):
    username = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget = forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'password')

class ClienteForm(forms.ModelForm):
	razao_social_ou_nome = forms.CharField(required=True)
	nome_fantasia = forms.CharField(required=False)
	codigo = forms.CharField(required=False)
	tipo_pessoa = forms.CharField(required=False)
	cnpj = forms.CharField(required=False)
	cpf = forms.CharField(required=False)
	email = forms.CharField(required=False)
	telefone = forms.CharField(required=False)
	inscricao_estadual = forms.CharField(required=False)
	suframa = forms.CharField(required=False)
	endereco = forms.CharField(required=False)
	complemento = forms.CharField(required=False)
	bairro = forms.CharField(required=False)
	cep = forms.CharField(required=False)
	cidade = forms.CharField(required=False)
	estado = forms.CharField(required=False)
	website = forms.CharField(required=False)
	observacoes = forms.CharField(required=False)
	status = forms.CharField(required=False)

	class Meta:
		model = Cliente
		exclude = ('usuario_criacao', 'data_criacao', 'usuario_modificacao', 'data_modificacao', 'conta_sistema')
		fields = ('razao_social_ou_nome', 'nome_fantasia', 'codigo', 'tipo_pessoa', 'cnpj', 'cpf', 'telefone', 'email', 'inscricao_estadual', 'suframa', 'endereco', 'complemento', 'bairro', 'cep', 'cidade', 'estado', 'website', 'observacoes', 'status')

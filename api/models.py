# coding=utf8
# -*- coding: utf8 -*-
# vim: set fileencoding=utf8 :

import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class ContaSistema(models.Model):
    nome = models.CharField(max_length=200, null=True, blank=True)
    usuario_criacao = models.ForeignKey(User, null=True, related_name='usr_criacao_empresa', editable=False)
    data_criacao = models.DateTimeField(null=True, auto_now_add=True, editable=False)
    usuario_modificacao = models.ForeignKey(User, null=True, related_name='usr_modificacao_empresa', editable=False)
    data_modificacao = models.DateTimeField(null=True, auto_now=True)

    def __str__(self):
        return self.nome

class UserProfile(models.Model):
	conta_sistema = models.ForeignKey(ContaSistema)
	user = models.ForeignKey(User)

	def __str__(self):
		return self.user.username

class Cliente(models.Model):
    conta_sistema = models.ForeignKey(ContaSistema, null=True, on_delete=models.PROTECT)
    razao_social_ou_nome = models.CharField(max_length=200, null=True)
    nome_fantasia = models.CharField(max_length=200, null=True)
    codigo = models.CharField(max_length=200, null=True, blank=True)
    tipo_pessoa = models.CharField(max_length=20, null=True, blank=True)
    cnpj = models.CharField(max_length=200, null=True, blank=True)
    cpf = models.CharField(max_length=200, null=True, blank=True)
    telefone = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=254, null=True, blank=True)
    inscricao_estadual = models.CharField(max_length=200, null=True, blank=True)
    suframa = models.CharField(max_length=200, null=True, blank=True)
    endereco = models.CharField(max_length=200, null=True, blank=True)
    complemento = models.CharField(max_length=200, null=True, blank=True)
    bairro = models.CharField(max_length=200, null=True, blank=True)
    cep = models.CharField(max_length=200, null=True, blank=True)
    cidade = models.CharField(max_length=200, null=True, blank=True)
    estado = models.CharField(max_length=200, null=True, blank=True)
    website = models.CharField(max_length=200, null=True, blank=True)
    status = models.CharField(max_length=200, null=True, blank=True)
    observacoes = models.TextField(null=True, blank=True)
    usuario_criacao = models.ForeignKey(User, null=True, related_name='usr_criacao_cliente', editable=False)
    data_criacao = models.DateTimeField(null=True, auto_now_add=True, editable=False)
    usuario_modificacao = models.ForeignKey(User, null=True, related_name='usr_modificacao_cliente')
    data_modificacao = models.DateTimeField(null=True, auto_now=True)

    def __str__(self):
        return self.razao_social_ou_nome

class ContatosClientes(models.Model):
    conta_sistema = models.ForeignKey(ContaSistema, null=True, on_delete=models.PROTECT)
    cliente = models.ForeignKey(Cliente, max_length=200, null=True, blank=True)
    nome = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=254, null=True, blank=True)
    telefone =  models.CharField(max_length=200, null=True, blank=True)
    cargo =  models.CharField(max_length=200, null=True, blank=True)
    usuario_criacao = models.ForeignKey(User, null=True, related_name='usr_criacao_contato_cliente', editable=False)
    data_criacao = models.DateTimeField(null=True, auto_now_add=True, editable=False)
    usuario_modificacao = models.ForeignKey(User, null=True, related_name='usr_modificacao_contato_cliente', editable=False)
    data_modificacao = models.DateTimeField(null=True, auto_now=True, editable=False)

    def __str__(self):
        return self.nome
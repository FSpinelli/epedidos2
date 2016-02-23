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
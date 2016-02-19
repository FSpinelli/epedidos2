from __future__ import unicode_literals
# coding=utf8
# -*- coding: utf8 -*-
# vim: set fileencoding=utf8 :

import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class AccountSystem(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
	account_system = models.ForeignKey(AccountSystem, null=True, on_delete=models.PROTECT)
	user = models.OneToOneField(User)
	access_token = models.CharField(max_length=255, null=True, blank=True)

	def __str__(self):
		return self.user.username
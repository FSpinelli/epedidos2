# coding=utf8
# -*- coding: utf8 -*-
# vim: set fileencoding=utf8 :

from django.contrib import admin
from django.contrib.auth.models import Permission
from .models import *

admin.site.register(ContaSistema)
admin.site.register(UserProfile)
admin.site.register(Cliente)
from django.contrib import admin
from django.contrib.auth.models import Permission
from .models import *

admin.site.register(ContaSistema)
admin.site.register(UserProfile)
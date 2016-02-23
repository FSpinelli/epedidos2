 	# coding=utf8
# -*- coding: utf8 -*-
# vim: set fileencoding=utf8 :

from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from django import forms

class CadastroForm(forms.ModelForm):
    username = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control', 'type': 'email', 'placeholder':'E-mail'}))
    password = forms.CharField(widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'Senha'}))

    class Meta:
        model = User
        fields = ('username', 'password')
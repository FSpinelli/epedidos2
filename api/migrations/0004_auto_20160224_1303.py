# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-24 16:03
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0003_auto_20160223_1204'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('razao_social_ou_nome', models.CharField(max_length=200, null=True)),
                ('nome_fantasia', models.CharField(max_length=200, null=True)),
                ('codigo', models.CharField(blank=True, max_length=200, null=True)),
                ('tipo_pessoa', models.CharField(blank=True, max_length=20, null=True)),
                ('cnpj', models.CharField(blank=True, max_length=200, null=True)),
                ('cpf', models.CharField(blank=True, max_length=200, null=True)),
                ('telefone', models.CharField(blank=True, max_length=200, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('inscricao_estadual', models.CharField(blank=True, max_length=200, null=True)),
                ('suframa', models.CharField(blank=True, max_length=200, null=True)),
                ('endereco', models.CharField(blank=True, max_length=200, null=True)),
                ('complemento', models.CharField(blank=True, max_length=200, null=True)),
                ('bairro', models.CharField(blank=True, max_length=200, null=True)),
                ('cep', models.CharField(blank=True, max_length=200, null=True)),
                ('cidade', models.CharField(blank=True, max_length=200, null=True)),
                ('estado', models.CharField(blank=True, max_length=200, null=True)),
                ('website', models.CharField(blank=True, max_length=200, null=True)),
                ('status', models.CharField(blank=True, max_length=200, null=True)),
                ('observacoes', models.TextField(blank=True, null=True)),
                ('data_criacao', models.DateTimeField(auto_now_add=True, null=True)),
                ('data_modificacao', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='contasistema',
            name='usuario_modificacao',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='usr_modificacao_empresa', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='conta_sistema',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.ContaSistema'),
        ),
        migrations.AddField(
            model_name='cliente',
            name='conta_sistema',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='api.ContaSistema'),
        ),
        migrations.AddField(
            model_name='cliente',
            name='usuario_criacao',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='usr_criacao_cliente', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='cliente',
            name='usuario_modificacao',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='usr_modificacao_cliente', to=settings.AUTH_USER_MODEL),
        ),
    ]

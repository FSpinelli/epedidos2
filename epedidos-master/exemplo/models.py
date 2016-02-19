# coding=utf8
# -*- coding: utf8 -*-
# vim: set fileencoding=utf8 :

import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class ContaSistema(models.Model):
    nome = models.CharField(max_length=200, null=True, blank=True)
    tipo = models.CharField(max_length=200, null=True, blank=True)
    estado = models.CharField(max_length=50, null=True, blank=True)
    usuario_criacao = models.ForeignKey(User, null=True, related_name='usr_criacao_empresa', editable=False)
    data_criacao = models.DateTimeField(null=True, auto_now_add=True, editable=False)
    usuario_modificacao = models.ForeignKey(User, null=True, related_name='usr_modificacao_empresa')
    data_modificacao = models.DateTimeField(null=True, auto_now=True)

    def __str__(self):
        return self.nome

class UserProfile(models.Model):
	conta_sistema = models.ForeignKey(ContaSistema, null=True, on_delete=models.PROTECT)
	user = models.OneToOneField(User)
	first_name = models.CharField(max_length=200, null=True, blank=True)
	last_name = models.CharField(max_length=200, null=True, blank=True) 
	telefone = models.CharField(max_length=200, null=True, blank=True)
	assinatura_email = models.TextField(null=True, blank=True)
	picture = models.FileField(null=True, blank=True, upload_to='pictures/profile')

	class Meta:
		permissions = (
			('view_usuario', 'Can view usuario'),
		)

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

	class Meta:
		permissions = (
			('view_cliente', 'Can view cliente'),
			('self_cliente', 'Can self cliente'),
		)

	def __str__(self):
		return self.razao_social_ou_nome


class ContatosClientes(models.Model):
	conta_sistema = models.ForeignKey(ContaSistema, null=True, on_delete=models.PROTECT)
	cliente = models.ForeignKey(Cliente, max_length=200, null=True, blank=True)
	nome1 = models.CharField(max_length=200, null=True, blank=True)
	nome2 = models.CharField(max_length=200, null=True, blank=True)
	nome3 = models.CharField(max_length=200, null=True, blank=True)
	nome4 = models.CharField(max_length=200, null=True, blank=True)
	email1 = models.EmailField(max_length=254, null=True, blank=True)
	email2 = models.EmailField(max_length=254, null=True, blank=True)
	email3 = models.EmailField(max_length=254, null=True, blank=True)
	email4 = models.EmailField(max_length=254, null=True, blank=True)
	telefone1 =  models.CharField(max_length=200, null=True, blank=True)
	telefone2 =  models.CharField(max_length=200, null=True, blank=True)
	telefone3 =  models.CharField(max_length=200, null=True, blank=True)
	telefone4 =  models.CharField(max_length=200, null=True, blank=True)
	cargo1 =  models.CharField(max_length=200, null=True, blank=True)
	cargo2 =  models.CharField(max_length=200, null=True, blank=True)
	cargo3 =  models.CharField(max_length=200, null=True, blank=True)
	cargo4 =  models.CharField(max_length=200, null=True, blank=True)
	usuario_criacao = models.ForeignKey(User, null=True, related_name='usr_criacao_contato_cliente', editable=False)
	data_criacao = models.DateTimeField(null=True, auto_now_add=True, editable=False)
	usuario_modificacao = models.ForeignKey(User, null=True, related_name='usr_modificacao_contato_cliente', editable=False)
	data_modificacao = models.DateTimeField(null=True, auto_now=True, editable=False)

	def __str__(self):
		return self.nome1

class Representada(models.Model):
	conta_sistema = models.ForeignKey(ContaSistema, null=True, on_delete=models.PROTECT)
	razao_social = models.CharField(max_length=200, null=True)
	nome_fantasia = models.CharField(max_length=200, null=True)
	cnpj = models.CharField(max_length=200, null=True, blank=True)
	telefone = models.CharField(max_length=200, null=True, blank=True)
	email = models.EmailField(max_length=254, null=True, blank=True)
	inscricao_estadual = models.CharField(max_length=200, null=True, blank=True)
	comissao = models.CharField(max_length=10, null=True, blank=True)
	pagamento_comissao = models.CharField(max_length=200, null=True, blank=True)
	observacoes = models.TextField(null=True, blank=True)
	usuario_criacao = models.ForeignKey(User, null=True, related_name='usr_criacao_representada', editable=False)
	data_criacao = models.DateTimeField(null=True, auto_now_add=True, editable=False)
	usuario_modificacao = models.ForeignKey(User, null=True, related_name='usr_modificacao_representada')
	data_modificacao = models.DateTimeField(null=True, auto_now=True)

	class Meta:
		permissions = (
			('view_representada', 'Can view representada'),
		)

	def __str__(self):
		return self.razao_social

class ContatosRepresentadas(models.Model):
	conta_sistema = models.ForeignKey(ContaSistema, null=True, on_delete=models.PROTECT)
	representada = models.ForeignKey(Representada, max_length=200, null=True, blank=True)
	nome1 = models.CharField(max_length=200, null=True, blank=True)
	nome2 = models.CharField(max_length=200, null=True, blank=True)
	nome3 = models.CharField(max_length=200, null=True, blank=True)
	nome4 = models.CharField(max_length=200, null=True, blank=True)
	email1 = models.EmailField(max_length=254, null=True, blank=True)
	email2 = models.EmailField(max_length=254, null=True, blank=True)
	email3 = models.EmailField(max_length=254, null=True, blank=True)
	email4 = models.EmailField(max_length=254, null=True, blank=True)
	telefone1 =  models.CharField(max_length=200, null=True, blank=True)
	telefone2 =  models.CharField(max_length=200, null=True, blank=True)
	telefone3 =  models.CharField(max_length=200, null=True, blank=True)
	telefone4 =  models.CharField(max_length=200, null=True, blank=True)
	cargo1 =  models.CharField(max_length=200, null=True, blank=True)
	cargo2 =  models.CharField(max_length=200, null=True, blank=True)
	cargo3 =  models.CharField(max_length=200, null=True, blank=True)
	cargo4 =  models.CharField(max_length=200, null=True, blank=True)
	usuario_criacao = models.ForeignKey(User, null=True, related_name='usr_criacao_contato_representada', editable=False)
	data_criacao = models.DateTimeField(null=True, auto_now_add=True, editable=False)
	usuario_modificacao = models.ForeignKey(User, null=True, related_name='usr_modificacao_contato_representada', editable=False)
	data_modificacao = models.DateTimeField(null=True, auto_now=True, editable=False)

	def __str__(self):
		return self.nome1

class Transportadora(models.Model):
	conta_sistema = models.ForeignKey(ContaSistema, null=True, on_delete=models.PROTECT)
	nome_fantasia = models.CharField(max_length=200, null=True)
	razao_social = models.CharField(max_length=200, null=True, blank=True)
	cnpj = models.CharField(max_length=200, null=True, blank=True)
	telefone = models.CharField(max_length=200, null=True, blank=True)
	email = models.EmailField(max_length=254, null=True, blank=True)
	inscricao_estadual = models.CharField(max_length=200, null=True, blank=True)
	inscricao_municipal = models.CharField(max_length=200, null=True, blank=True)
	endereco = models.CharField(max_length=200, null=True, blank=True)
	complemento = models.CharField(max_length=200, null=True, blank=True)
	bairro = models.CharField(max_length=200, null=True, blank=True)
	cep = models.CharField(max_length=200, null=True, blank=True)
	cidade = models.CharField(max_length=200, null=True, blank=True)
	estado = models.CharField(max_length=200, null=True, blank=True)
	website = models.CharField(max_length=200, null=True, blank=True)
	observacoes = models.TextField(null=True, blank=True)
	usuario_criacao = models.ForeignKey(User, null=True, related_name='usr_criacao_transportadora', editable=False)
	data_criacao = models.DateTimeField(null=True, auto_now_add=True, editable=False)
	usuario_modificacao = models.ForeignKey(User, null=True, related_name='usr_modificacao_transportadora')
	data_modificacao = models.DateTimeField(null=True, auto_now=True)

	class Meta:
		permissions = (
			('view_transportadora', 'Can view transportadora'),
		)

	def __str__(self):
		return self.nome_fantasia

class ContatosTransportadoras(models.Model):
	conta_sistema = models.ForeignKey(ContaSistema, null=True, on_delete=models.PROTECT)
	transportadora = models.ForeignKey(Transportadora, max_length=200, null=True, blank=True)
	nome1 = models.CharField(max_length=200, null=True, blank=True)
	nome2 = models.CharField(max_length=200, null=True, blank=True)
	nome3 = models.CharField(max_length=200, null=True, blank=True)
	nome4 = models.CharField(max_length=200, null=True, blank=True)
	email1 = models.EmailField(max_length=254, null=True, blank=True)
	email2 = models.EmailField(max_length=254, null=True, blank=True)
	email3 = models.EmailField(max_length=254, null=True, blank=True)
	email4 = models.EmailField(max_length=254, null=True, blank=True)
	telefone1 =  models.CharField(max_length=200, null=True, blank=True)
	telefone2 =  models.CharField(max_length=200, null=True, blank=True)
	telefone3 =  models.CharField(max_length=200, null=True, blank=True)
	telefone4 =  models.CharField(max_length=200, null=True, blank=True)
	cargo1 =  models.CharField(max_length=200, null=True, blank=True)
	cargo2 =  models.CharField(max_length=200, null=True, blank=True)
	cargo3 =  models.CharField(max_length=200, null=True, blank=True)
	cargo4 =  models.CharField(max_length=200, null=True, blank=True)
	usuario_criacao = models.ForeignKey(User, null=True, related_name='usr_criacao_contato_transportadora', editable=False)
	data_criacao = models.DateTimeField(null=True, auto_now_add=True, editable=False)
	usuario_modificacao = models.ForeignKey(User, null=True, related_name='usr_modificacao_contato_transportadora', editable=False)
	data_modificacao = models.DateTimeField(null=True, auto_now=True, editable=False)

	def __str__(self):
		return self.nome1

class Produto(models.Model):
	conta_sistema = models.ForeignKey(ContaSistema, null=True, on_delete=models.PROTECT)
	representada = models.ForeignKey(Representada, max_length=200, null=True)
	nome = models.CharField(max_length=200, null=True)
	preco_tabela = models.CharField(max_length=200, null=True)
	preco_promocao = models.CharField(max_length=200, null=True, blank=True)
	foto = models.CharField(max_length=200, null=True, blank=True)
	codigo = models.CharField(max_length=200, null=True, blank=True)
	unidade = models.CharField(max_length=20, null=True, blank=True)
	ipi = models.CharField(max_length=100, null=True, blank=True)
	substituicao_tributaria = models.CharField(max_length=10, null=True, blank=True)
	# comissao = models.CharField(max_length=10, null=True, blank=True)
	# moeda = models.CharField(max_length=10, null=True, blank=True)
	observacoes = models.TextField(null=True, blank=True)
	usuario_criacao = models.ForeignKey(User, null=True, related_name='usr_criacao_produto', editable=False)
	data_criacao = models.DateTimeField(null=True, auto_now_add=True, editable=False)
	usuario_modificacao = models.ForeignKey(User, null=True, related_name='usr_modificacao_produto')
	data_modificacao = models.DateTimeField(null=True, auto_now=True)

	class Meta:
		permissions = (
			('view_produto', 'Can view produto'),
			('self_produto', 'Can self produto'),
		)

	def __str__(self):
		return self.nome

class TamanhoProduto(models.Model):
	conta_sistema = models.ForeignKey(ContaSistema, null=True, on_delete=models.PROTECT)
	produto = models.ForeignKey(Produto, max_length=200, null=True, blank=True)
	tamanho = models.CharField(max_length=50, null=True, blank=True)
	usuario_criacao = models.ForeignKey(User, null=True, related_name='usr_criacao_tamanho_produto', editable=False)
	data_criacao = models.DateTimeField(null=True, auto_now_add=True, editable=False)
	usuario_modificacao = models.ForeignKey(User, null=True, related_name='usr_modificacao_tamanho_produto', editable=False)
	data_modificacao = models.DateTimeField(null=True, auto_now=True, editable=False)

	def __str__(self):
		return self.tamanho

class CorProduto(models.Model):
	conta_sistema = models.ForeignKey(ContaSistema, null=True, on_delete=models.PROTECT)
	produto = models.ForeignKey(Produto, max_length=200, null=True, blank=True)
	cor = models.CharField(max_length=50, null=True, blank=True)
	usuario_criacao = models.ForeignKey(User, null=True, related_name='usr_criacao_cor_produto', editable=False)
	data_criacao = models.DateTimeField(null=True, auto_now_add=True, editable=False)
	usuario_modificacao = models.ForeignKey(User, null=True, related_name='usr_modificacao_cor_produto', editable=False)
	data_modificacao = models.DateTimeField(null=True, auto_now=True, editable=False)

	def __str__(self):
		return self.cor

class Pedido(models.Model):
	conta_sistema = models.ForeignKey(ContaSistema, null=True, on_delete=models.PROTECT)
	cliente = models.ForeignKey(Cliente, null=True, on_delete=models.PROTECT)
	representada = models.ForeignKey(Representada, null=True, on_delete=models.PROTECT)
	condicao_pagamento = models.CharField(max_length=200, null=True)
	numero_pedido = models.CharField(max_length=200, null=True)
	data_emissao = models.DateField(null=True)
	vendedor = models.ForeignKey(UserProfile, null=True, on_delete=models.PROTECT)
	transportadora = models.ForeignKey(Transportadora, null=True, blank=True)
	contato_cliente = models.CharField(max_length=200, null=True, blank=True)
	observacoes = models.TextField(null=True, blank=True)
	usuario_criacao = models.ForeignKey(User, null=True, related_name='usr_criacao_pedido', editable=False)
	data_criacao = models.DateTimeField(null=True, auto_now_add=True, editable=False)
	usuario_modificacao = models.ForeignKey(User, null=True, related_name='usr_modificacao_pedido')
	data_modificacao = models.DateTimeField(null=True, auto_now=True)

	class Meta:
		permissions = (
			('view_pedido', 'Can view pedido'),
			('self_pedido', 'Can self pedido'),
		)

	def __str__(self):
		return self.numero_pedido

class ProdutosPedidos(models.Model):
	conta_sistema = models.ForeignKey(ContaSistema, null=True, on_delete=models.PROTECT)
	pedido = models.ForeignKey(Pedido, max_length=200, null=True)
	produto = models.ForeignKey(Produto, max_length=200, null=True)
	quantidade = models.CharField(max_length=200, null=True)
	tabela_preco = models.CharField(max_length=200, null=True)
	tipo_preco = models.CharField(max_length=200, null=True)
	desconto = models.CharField(max_length=200, null=True, blank=True)
	preco_liquido = models.CharField(max_length=200, null=True, blank=True)
	observacoes = models.TextField(null=True, blank=True)

	# def __str__(self):
	# 	return self.produto

class Agenda(models.Model):
	conta_sistema = models.ForeignKey(ContaSistema, null=True, on_delete=models.PROTECT)
	tipo = models.CharField(max_length=200, null=True)
	title = models.CharField(max_length=200, null=True)
	start = models.CharField(max_length=200, null=True)
	local = models.CharField(max_length=200, null=True, blank=True)
	responsavel = models.ForeignKey(UserProfile, null=True, on_delete=models.PROTECT)
	observacoes = models.TextField(null=True, blank=True)
	usuario_criacao = models.ForeignKey(User, null=True, related_name='usr_criacao_agenda', editable=False)
	data_criacao = models.DateTimeField(null=True, auto_now_add=True, editable=False)
	usuario_modificacao = models.ForeignKey(User, null=True, related_name='usr_modificacao_agenda')
	data_modificacao = models.DateTimeField(null=True, auto_now=True)

	class Meta:
		permissions = (
			('view_agenda', 'Can view agenda'),
			('self_agenda', 'Can self agenda'),
		)

	def __str__(self):
		return self.title

class ClientesVendedor(models.Model):
	conta_sistema = models.ForeignKey(ContaSistema, null=True, on_delete=models.PROTECT)
	vendedor = models.ForeignKey(UserProfile, null=True, on_delete=models.PROTECT)
	cliente = models.ForeignKey(Cliente, null=True, on_delete=models.PROTECT)
	usuario_criacao = models.ForeignKey(User, null=True, related_name='usr_criacao_clientes_vendedor', editable=False)
	data_criacao = models.DateTimeField(null=True, auto_now_add=True, editable=False)
	usuario_modificacao = models.ForeignKey(User, null=True, related_name='usr_modificacao_clientes_vendedor')
	data_modificacao = models.DateTimeField(null=True, auto_now=True)

	def __str__(self):
		return str(self.cliente)

class RepresentadasVendedor(models.Model):
	conta_sistema = models.ForeignKey(ContaSistema, null=True, on_delete=models.PROTECT)
	vendedor = models.ForeignKey(UserProfile, null=True, on_delete=models.PROTECT)
	representada = models.ForeignKey(Representada, null=True, on_delete=models.PROTECT)
	comissao = models.FloatField(null=True)
	usuario_criacao = models.ForeignKey(User, null=True, related_name='usr_criacao_representada_vendedor', editable=False)
	data_criacao = models.DateTimeField(null=True, auto_now_add=True, editable=False)
	usuario_modificacao = models.ForeignKey(User, null=True, related_name='usr_modificacao_representada_vendedor')
	data_modificacao = models.DateTimeField(null=True, auto_now=True)

	def __str__(self):
		return str(self.representada)
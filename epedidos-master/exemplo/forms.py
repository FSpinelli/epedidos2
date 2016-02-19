 	# coding=utf8
# -*- coding: utf8 -*-
# vim: set fileencoding=utf8 :

from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from django import forms
from web.models import *

ESTADOS_BRASILEIROS = (('', 'Selecione'), ('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'), ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espirito Santo'), ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MS', 'Mato Grosso do Sul'), ('MT', 'Mato Grosso'), ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'), ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'), ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'), ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins'))


class CadastroForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control', 'type': 'email'}))
    password = forms.CharField(widget = forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password')

class ConfigInicialForm(forms.ModelForm):
	TIPO_EMPRESA = (('Representação Comercial', 'Representação Comercial'), ('Distribuição', 'Distribuição'), ('Indústria', 'Indústria'))

	tipo = forms.ChoiceField(label='', choices=TIPO_EMPRESA , widget=forms.RadioSelect)
	nome = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control'}))
	estado = forms.ChoiceField(label='', choices=ESTADOS_BRASILEIROS, widget=forms.Select(attrs={'class':'form-control m-b'}))
	
	class Meta:
		model = ContaSistema
		exclude = ('usuario_criacao', 'usuario_modificacao')
        fields = ('nome', 'estado', 'tipo',)

class ClienteForm(forms.ModelForm):
	TIPO_PESSOA = (('Pessoa Jurídica', 'Pessoa Juridica'), ('Pessoa Física', 'Pessoa Física'))
	STATUS = (('A', 'Ativo'), ('I', 'Inativo'))
	
	razao_social_ou_nome = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}))
	nome_fantasia = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control'}), required=False)
	codigo = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control'}), required=False)
	tipo_pessoa = forms.ChoiceField(choices=TIPO_PESSOA , widget=forms.RadioSelect, required=False, initial=1)
	cnpj = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control'}), required=False)
	cpf = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control'}), required=False)
	email = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control', 'type': 'email', 'pattern': '[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,3}$', 'title': 'Ex.: nome@exemplo.com.br'}), required=False)
	telefone = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control', 'maxlength': '15','onkeypress': 'mascaraTel(this)'}), required=False)
	inscricao_estadual = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control'}), required=False)
	suframa = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control'}), required=False)
	endereco = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control'}), required=False)
	complemento = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control'}), required=False)
	bairro = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control'}), required=False)
	cep = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control'}), required=False)
	cidade = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control'}), required=False)
	estado = forms.ChoiceField(label='', choices=ESTADOS_BRASILEIROS, widget=forms.Select(attrs={'class':'form-control m-b'}), required=False)
	website = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control'}), required=False)
	observacoes = forms.CharField(widget = forms.Textarea(attrs={'class': 'form-control', 'rows':'5'}), required=False)
	status = forms.ChoiceField(label='', choices=STATUS, widget=forms.Select(attrs={'class':'form-control m-b'}), required=False)

	class Meta:
		model = Cliente
		exclude = ('usuario_criacao', 'data_criacao', 'usuario_modificacao', 'data_modificacao', 'conta_sistema')
		fields = ('razao_social_ou_nome', 'nome_fantasia', 'codigo', 'tipo_pessoa', 'cnpj', 'cpf', 'telefone', 'email', 'inscricao_estadual', 'suframa', 'endereco', 'complemento', 'bairro', 'cep', 'cidade', 'estado', 'website', 'status', 'observacoes')

class ContatoClienteForm(forms.ModelForm):
	nome1 = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Nome'}), required=False)
	nome2 = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Nome'}), required=False)
	nome3 = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Nome'}), required=False)
	nome4 = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Nome'}), required=False)
	email1 = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder':'E-mail', 'type': 'email', 'pattern': '[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,3}$', 'title': 'Ex.: nome@exemplo.com.br'}), required=False)
	email2 = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder':'E-mail', 'type': 'email', 'pattern': '[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,3}$', 'title': 'Ex.: nome@exemplo.com.br'}), required=False)
	email3 = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder':'E-mail', 'type': 'email', 'pattern': '[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,3}$', 'title': 'Ex.: nome@exemplo.com.br'}), required=False)
	email4 = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder':'E-mail', 'type': 'email', 'pattern': '[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,3}$', 'title': 'Ex.: nome@exemplo.com.br'}), required=False)
	telefone1 = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Telefone', 'maxlength': '15','onkeypress': 'mascaraTel(this)'}), required=False)
	telefone2 = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Telefone', 'maxlength': '15','onkeypress': 'mascaraTel(this)'}), required=False)
	telefone3 = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Telefone', 'maxlength': '15','onkeypress': 'mascaraTel(this)'}), required=False)
	telefone4 = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Telefone', 'maxlength': '15','onkeypress': 'mascaraTel(this)'}), required=False)
	cargo1 = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Cargo'}), required=False)
	cargo2 = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Cargo'}), required=False)
	cargo3 = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Cargo'}), required=False)
	cargo4 = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Cargo'}), required=False)

	class Meta:
		model = ContatosClientes
		exclude = ('conta_sistema', 'cliente', 'usuario_criacao', 'data_criacao', 'usuario_modificacao', 'data_modificacao')
		fields = ('nome1', 'nome2', 'nome3', 'nome4', 'email1', 'email2', 'email3', 'email4', 'telefone1', 'telefone2', 'telefone3', 'telefone4', 'cargo1', 'cargo2', 'cargo3', 'cargo4')

class RepresentadaForm(forms.ModelForm):
	PAGAMENTO_COMISSAO = (('1', 'Paga comissão parcelada na liquidez do pedido'), ('2', 'Paga comissão em parcela única'))

	razao_social = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}))
	nome_fantasia = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}))
	cnpj = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control'}), required=False)
	email = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control', 'type': 'email', 'pattern': '[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,3}$', 'title': 'Ex.: nome@exemplo.com.br'}), required=False)
	telefone = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control', 'maxlength': '15','onkeypress': 'mascaraTel(this)'}), required=False)
	inscricao_estadual = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control'}), required=False)
	comissao = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control'}))
	pagamento_comissao = forms.ChoiceField(label='', choices=PAGAMENTO_COMISSAO , widget=forms.RadioSelect, initial=1)
	observacoes = forms.CharField(widget = forms.Textarea(attrs={'class': 'form-control', 'rows':'5'}), required=False)

	class Meta:
		model = Representada
		exclude = ('usuario_criacao', 'data_criacao', 'usuario_modificacao', 'data_modificacao', 'conta_sistema')
		fields = ('razao_social', 'nome_fantasia', 'cnpj', 'telefone', 'email', 'inscricao_estadual', 'comissao', 'pagamento_comissao', 'observacoes')

class ContatoRepresentadaForm(forms.ModelForm):
	nome1 = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Nome'}), required=False)
	nome2 = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Nome'}), required=False)
	nome3 = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Nome'}), required=False)
	nome4 = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Nome'}), required=False)
	email1 = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder':'E-mail', 'type': 'email', 'pattern': '[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,3}$', 'title': 'Ex.: nome@exemplo.com.br'}), required=False)
	email2 = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder':'E-mail', 'type': 'email', 'pattern': '[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,3}$', 'title': 'Ex.: nome@exemplo.com.br'}), required=False)
	email3 = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder':'E-mail', 'type': 'email', 'pattern': '[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,3}$', 'title': 'Ex.: nome@exemplo.com.br'}), required=False)
	email4 = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder':'E-mail', 'type': 'email', 'pattern': '[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,3}$', 'title': 'Ex.: nome@exemplo.com.br'}), required=False)
	telefone1 = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Telefone', 'maxlength': '15','onkeypress': 'mascaraTel(this)'}), required=False)
	telefone2 = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Telefone', 'maxlength': '15','onkeypress': 'mascaraTel(this)'}), required=False)
	telefone3 = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Telefone', 'maxlength': '15','onkeypress': 'mascaraTel(this)'}), required=False)
	telefone4 = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Telefone', 'maxlength': '15','onkeypress': 'mascaraTel(this)'}), required=False)
	cargo1 = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Cargo'}), required=False)
	cargo2 = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Cargo'}), required=False)
	cargo3 = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Cargo'}), required=False)
	cargo4 = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Cargo'}), required=False)

	class Meta:
		model = ContatosRepresentadas
		exclude = ('conta_sistema', 'cliente', 'usuario_criacao', 'data_criacao', 'usuario_modificacao', 'data_modificacao')
		fields = ('nome1', 'nome2', 'nome3', 'nome4', 'email1', 'email2', 'email3', 'email4', 'telefone1', 'telefone2', 'telefone3', 'telefone4', 'cargo1', 'cargo2', 'cargo3', 'cargo4')

class TransportadoraForm(forms.ModelForm):
	PAGAMENTO_COMISSAO = (('1', 'Paga comissão parcelada na liquidez do pedido'), ('2', 'Paga comissão em parcela única'))

	nome_fantasia = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}))
	razao_social = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control'}), required=False)
	cnpj = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control'}), required=False)
	email = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control', 'type': 'email', 'pattern': '[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,3}$', 'title': 'Ex.: nome@exemplo.com.br'}), required=False)
	telefone = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control', 'maxlength': '15','onkeypress': 'mascaraTel(this)'}), required=False)
	inscricao_estadual = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control'}), required=False)
	inscricao_municipal = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control'}), required=False)
	endereco = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control'}), required=False)
	complemento = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control'}), required=False)
	bairro = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control'}), required=False)
	cep = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control'}), required=False)
	cidade = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control'}), required=False)
	estado = forms.ChoiceField(label='', choices=ESTADOS_BRASILEIROS, widget=forms.Select(attrs={'class':'form-control m-b'}), required=False)
	website = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control'}), required=False)
	observacoes = forms.CharField(widget = forms.Textarea(attrs={'class': 'form-control', 'rows':'5'}), required=False)

	class Meta:
		model = Transportadora
		exclude = ('usuario_criacao', 'data_criacao', 'usuario_modificacao', 'data_modificacao', 'conta_sistema')
		fields = ('nome_fantasia', 'razao_social', 'cnpj', 'telefone', 'email', 'inscricao_estadual', 'inscricao_municipal', 'endereco', 'complemento', 'bairro', 'cep', 'cidade', 'estado', 'website', 'observacoes')

class ContatoTransportadoraForm(forms.ModelForm):
	nome1 = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Nome'}), required=False)
	nome2 = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Nome'}), required=False)
	nome3 = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Nome'}), required=False)
	nome4 = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Nome'}), required=False)
	email1 = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder':'E-mail', 'type': 'email', 'pattern': '[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,3}$', 'title': 'Ex.: nome@exemplo.com.br'}), required=False)
	email2 = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder':'E-mail', 'type': 'email', 'pattern': '[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,3}$', 'title': 'Ex.: nome@exemplo.com.br'}), required=False)
	email3 = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder':'E-mail', 'type': 'email', 'pattern': '[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,3}$', 'title': 'Ex.: nome@exemplo.com.br'}), required=False)
	email4 = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder':'E-mail', 'type': 'email', 'pattern': '[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,3}$', 'title': 'Ex.: nome@exemplo.com.br'}), required=False)
	telefone1 = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Telefone', 'maxlength': '15','onkeypress': 'mascaraTel(this)'}), required=False)
	telefone2 = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Telefone', 'maxlength': '15','onkeypress': 'mascaraTel(this)'}), required=False)
	telefone3 = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Telefone', 'maxlength': '15','onkeypress': 'mascaraTel(this)'}), required=False)
	telefone4 = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Telefone', 'maxlength': '15','onkeypress': 'mascaraTel(this)'}), required=False)
	cargo1 = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Cargo'}), required=False)
	cargo2 = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Cargo'}), required=False)
	cargo3 = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Cargo'}), required=False)
	cargo4 = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Cargo'}), required=False)

	class Meta:
		model = ContatosTransportadoras
		exclude = ('conta_sistema', 'transportadora', 'usuario_criacao', 'data_criacao', 'usuario_modificacao', 'data_modificacao')
		fields = ('nome1', 'nome2', 'nome3', 'nome4', 'email1', 'email2', 'email3', 'email4', 'telefone1', 'telefone2', 'telefone3', 'telefone4', 'cargo1', 'cargo2', 'cargo3', 'cargo4')

class ProdutoForm(forms.ModelForm):
	# representada = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control'}))
	nome = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}))
	preco_tabela = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control', 'required': 'true', 'pattern': '[0-9 \.]*,[0-9][0-9]', 'title': 'Ex.: 100,00'}))
	preco_promocao = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control', 'pattern': '[0-9 \.]*,[0-9][0-9]', 'title': 'Ex.: 100,00'}), required=False)
	foto = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control'}), required=False)
	codigo = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control'}), required=False)
	unidade = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Unid, Kg, Pct, Cx...'}), required=False)
	ipi = forms.CharField(widget = forms.TextInput(attrs={'class': 'input-sm form-control', 'id': 'appendedInput'}), required=False)
	substituicao_tributaria = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control'}), required=False)
	observacoes = forms.CharField(widget = forms.Textarea(attrs={'class': 'form-control', 'rows':'5'}), required=False)

	class Meta:
		model = Produto
		exclude = ('usuario_criacao', 'data_criacao', 'usuario_modificacao', 'data_modificacao', 'conta_sistema')
		fields = ('representada', 'nome', 'preco_tabela', 'preco_promocao', 'foto', 'codigo', 'unidade', 'ipi', 'substituicao_tributaria', 'observacoes')

class PedidoForm(forms.ModelForm):
	condicao_pagamento = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Exemplo: 30/60/90', 'required': 'true'}))
	data_emissao = forms.DateField(widget = forms.TextInput(attrs={'class': 'form-control', 'size': '16', 'type': 'date', 'required': 'true'}))
	observacoes = forms.CharField(widget = forms.Textarea(attrs={'class': 'form-control', 'rows':'5'}), required=False)

	class Meta:
		model = Pedido
		exclude = ('usuario_criacao', 'data_criacao', 'usuario_modificacao', 'data_modificacao', 'conta_sistema')
		fields = ('cliente', 'representada', 'condicao_pagamento', 'numero_pedido', 'data_emissao', 'vendedor', 'transportadora', 'contato_cliente', 'observacoes')

class ProdutosPedidosForm(forms.ModelForm):
	quantidade = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control'}))
	desconto = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control'}), required=False)
	observacoes = forms.CharField(widget = forms.Textarea(attrs={'class': 'form-control', 'rows':'5'}), required=False)
	
	class Meta:
		model = ProdutosPedidos
		exclude = ('conta_sistema', 'pedido', 'produto')
		fields = ('quantidade', 'desconto', 'observacoes')

class AgendaForm(forms.ModelForm):
	TIPO_AGENDA= (('', 'Selecione'), ('V', 'Visita'), ('L', 'Ligação'), ('A', 'Atividade'))
	
	tipo = forms.ChoiceField(label='', choices=TIPO_AGENDA, widget=forms.Select(attrs={'class':'form-control m-b', 'required': 'true'}))
	title = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}))
	# start = forms.DateField(widget = forms.TextInput(attrs={'id':'dataEvento', 'class': 'form-control', 'size': '16', 'type': 'date', 'required': 'true'}))
	# hora = forms.TimeField(widget = forms.TextInput(attrs={'class': 'form-control', 'type': 'time'}), required=False)
	local = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control'}), required=False)
	observacoes = forms.CharField(widget = forms.Textarea(attrs={'class': 'form-control', 'rows':'5'}), required=False)

	class Meta:
		model = Agenda
		exclude = ('usuario_criacao', 'data_criacao', 'usuario_modificacao', 'data_modificacao', 'conta_sistema', 'responsavel', 'start')
		fields = ('tipo', 'title', 'local', 'observacoes')

class UsuarioForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}))
    last_name = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}))
    username = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control', 'type': 'email', 'pattern': '[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,3}$', 'title': 'Ex.: nome@exemplo.com.br', 'required': 'true'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username')

class UserProfileForm(forms.ModelForm):
	telefone = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control', 'id': 'id_telefone', 'maxlength': '15', 'onkeypress': 'mascaraTel(this)'}), required=False)
	picture = forms.FileField(label='Select a file', required=False)

	class Meta:
		model = UserProfile
		fields = ('telefone', 'picture')
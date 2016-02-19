# coding=utf8
# -*- coding: utf8 -*-
# vim: set fileencoding=utf8 :

from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, loader
from django.template.loader import render_to_string
from django.db import IntegrityError
from django.db.models import Max
from django.contrib.auth.models import User, Permission, Group
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import permission_required
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from random import choice
from web.models import *
from web.forms import *
from PIL import Image
import requests
import cgi

def cadastrar(request):
    if request.method == 'POST':
        cadastro_form = CadastroForm(data=request.POST)
        if cadastro_form.is_valid():
            cadastro = cadastro_form.save()
            cadastro.set_password(cadastro.password)
            cadastro.save()
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            auth_login(request, user)
            return HttpResponseRedirect('/configuracao_inicial/')
        else:
            print cadastro_form.errors
    else:
        cadastro_form = CadastroForm()
    return render(
    		request,
            'web/cadastrar.html',
            {'cadastro_form': cadastro_form})

@login_required
def configuracao_inicial(request):
	try:
		u = User.objects.get(pk=request.user.pk)
		user_profile = UserProfile.objects.get(user=u)
		return HttpResponseRedirect("/home/")
	except ObjectDoesNotExist:
		if request.method == 'POST':
			config_form = ConfigInicialForm(data=request.POST)
			if  config_form.is_valid():
				config = config_form.save(commit=False)
				u = User.objects.get(pk=request.user.pk)
				config.usuario_criacao = u
				config.usuario_modificacao = u
				config.save()

				conta_sistema=ContaSistema.objects.get(pk=config.pk)
				user_profile = UserProfile(user=u, conta_sistema=conta_sistema)
				user_profile.save()

				return HttpResponseRedirect('/home/')
			else:
				print config_form.errors
		else:        
			config_form = ConfigInicialForm()
		return render(
	    		request,
	            'web/configuracao_inicial.html', 
	            {'user':request.user, 'config_form':config_form})

def login(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user:
			if user.is_active:
				auth_login(request, user)
				if request.session['pag_login_required'] == "":
					return HttpResponseRedirect('/home/')
				else:
					return HttpResponseRedirect(request.session['pag_login_required'])
			else:
				context = {'mensagem':'Seu usuário está desativado.'}
		else:
			context = {'mensagem':'Usuário ou senha incorreta.'}
	else:
		context = {}
		if request.GET.get('next'):
			request.session['pag_login_required'] = request.GET['next']
		else:
			request.session['pag_login_required'] = ""
	return render(request, 'web/login.html', context)

@login_required
def user_logout(request):
	logout(request)
	return HttpResponseRedirect('/login/')

@login_required
def home(request):
	return render(
    		request,
            'web/home.html',
            {'user':request.user, 'class_home':'active'})

@login_required
def clientes(request):
	user = UserProfile.objects.get(user=request.user)
	lista_clientes = Cliente.objects.filter(conta_sistema=user.conta_sistema).order_by('data_criacao')
	if 'msg' in request.GET: msg = request.GET['msg']
	else: msg=''
	return render(
    		request,
            'web/clientes.html',
            {'user':request.user, 'class_clientes':'active', 'lista_clientes': lista_clientes, 'msg':msg})

@permission_required('web.add_cliente')
def cadastrar_clientes(request):
	if request.method == 'POST':
		cliente_form = ClienteForm(data=request.POST)
		contato_cliente_form = ContatoClienteForm(data=request.POST)
		if cliente_form.is_valid():
			cliente = cliente_form.save(commit=False)
			user = User.objects.get(pk=request.user.pk)
			cliente.usuario_criacao = user
			cliente.usuario_modificacao = user

			user_profile = UserProfile.objects.get(user=request.user)
			cliente.conta_sistema = user_profile.conta_sistema
			cliente.save()

			if contato_cliente_form.is_valid():
				contato = contato_cliente_form.save(commit=False)
				contato.conta_sistema = user_profile.conta_sistema
				contato.cliente = cliente
				contato.usuario_criacao = user
				contato.usuario_modificacao = user
				contato.save()

			return HttpResponseRedirect('/clientes/'+str(cliente.pk)+'/?msg=1')
		else:
			print cliente_form.errors
			print contato_cliente_form.errors
	else:
		cliente_form = ClienteForm()
		contato_cliente_form = ContatoClienteForm()
	return render(
    		request,
            'web/cadastrar_clientes.html',
            {'user':request.user, 'class_clientes':'active', 'cliente_form':cliente_form, 'contato_cliente_form':contato_cliente_form})

@login_required
def visualizar_clientes(request, cliente_id):
	user_profile = UserProfile.objects.get(user=request.user)
	cliente = get_object_or_404(Cliente, pk=cliente_id, conta_sistema=user_profile.conta_sistema)
	contatos_clientes = get_object_or_404(ContatosClientes, cliente=cliente, conta_sistema=user_profile.conta_sistema)
	cliente_form = ClienteForm()
	contato_cliente_form = ContatoClienteForm()
	if 'msg' in request.GET: msg = request.GET['msg']
	else: msg=''

	return render(
    		request,	
            'web/visualizar_clientes.html',
            {'user':request.user, 'class_clientes':'active', 'cliente':cliente, 'contatos_clientes':contatos_clientes, 'cliente_form':cliente_form, 'contato_cliente_form':contato_cliente_form, 'estados':ESTADOS_BRASILEIROS, 'status_cliente':ClienteForm.STATUS, 'msg':msg})

@permission_required('web.change_cliente')
def alterar_clientes(request, cliente_id):
	if request.method == 'POST':
		user_profile = UserProfile.objects.get(user=request.user)
		cliente = get_object_or_404(Cliente, pk=cliente_id, conta_sistema=user_profile.conta_sistema)
		cliente_form = ClienteForm(request.POST or None, instance=cliente)
		if cliente_form.is_valid():
			cliente = cliente_form.save(commit=False)
			user = User.objects.get(pk=request.user.pk)
			cliente.usuario_modificacao = user
			cliente.save()

			contato_cliente = get_object_or_404(ContatosClientes, cliente=cliente, conta_sistema=user_profile.conta_sistema)
			contato_cliente_form = ContatoClienteForm(request.POST or None, instance=contato_cliente)
			if contato_cliente_form.is_valid():
				contato = contato_cliente_form.save(commit=False)
				contato.usuario_modificacao = user
				contato.save()

			return HttpResponseRedirect('/clientes/'+str(cliente.pk)+'/?msg=2')
		else:
			cliente_form = ClienteForm()
			print cliente_form.errors
			return render(request, 'web/visualizar_clientes.html', {'user':request.user, 'class_clientes':'active', 'cliente':cliente, 'cliente_form':cliente_form})

@permission_required('web.delete_cliente')
def excluir_clientes(request, cliente_id):
	if request.method == 'POST':
	# try:
		get_object_or_404(Cliente, pk=cliente_id).delete()
		user = UserProfile.objects.get(user=request.user)
		lista_clientes = Cliente.objects.filter(conta_sistema=user.conta_sistema).order_by('data_criacao')
		return HttpResponseRedirect('/clientes/?msg=1')
	# except IntegrityError as ex:
	# 	message = _("form for customer xyz was successfully updated...")
	# 	request.user.message_set.create(message = message)
	# 	return HttpResponseRedirect('/clientes/')

@login_required
def representadas(request):
	user = UserProfile.objects.get(user=request.user)
	lista_representadas = Representada.objects.filter(conta_sistema=user.conta_sistema).order_by('data_criacao')
	if 'msg' in request.GET: msg = request.GET['msg']
	else: msg=''
	return render(
    		request,
            'web/representadas.html',
            {'user':request.user, 'class_representadas':'active', 'lista_representadas': lista_representadas, 'msg':msg})

@permission_required('web.add_representada')
def cadastrar_representadas(request):
	if request.method == 'POST':
		representada_form = RepresentadaForm(data=request.POST)
		contato_representada_form = ContatoRepresentadaForm(data=request.POST)
		if representada_form.is_valid():
			representada = representada_form.save(commit=False)
			user = User.objects.get(pk=request.user.pk)
			representada.usuario_criacao = user
			representada.usuario_modificacao = user

			user_profile = UserProfile.objects.get(user=request.user)
			representada.conta_sistema = user_profile.conta_sistema
			representada.save()

			if contato_representada_form.is_valid():
				contato = contato_representada_form.save(commit=False)
				contato.conta_sistema = user_profile.conta_sistema
				contato.representada = representada
				contato.usuario_criacao = user
				contato.usuario_modificacao = user
				contato.save()

			return HttpResponseRedirect('/representadas/'+str(representada.pk)+'/?msg=1')
		else:
			print representada_form.errors
			print contato_representada_form.errors
	else:
		representada_form = RepresentadaForm()
		contato_representada_form = ContatoRepresentadaForm()
	return render(
    		request,
            'web/cadastrar_representadas.html',
            {'user':request.user, 'class_representadas':'active', 'representada_form':representada_form, 'contato_representada_form':contato_representada_form})

@login_required
def visualizar_representadas(request, representada_id):
	user_profile = UserProfile.objects.get(user=request.user)
	representada = get_object_or_404(Representada, pk=representada_id, conta_sistema=user_profile.conta_sistema)
	contatos_representadas = get_object_or_404(ContatosRepresentadas, representada=representada, conta_sistema=user_profile.conta_sistema)
	representada_form = RepresentadaForm()
	contato_representada_form = ContatoRepresentadaForm()
	if 'msg' in request.GET: msg = request.GET['msg']
	else: msg=''

	return render(
    		request,	
            'web/visualizar_representadas.html',
            {'user':request.user, 'class_representadas':'active', 'representada':representada, 'contatos_representadas':contatos_representadas, 'representada_form':representada_form, 'contato_representada_form':contato_representada_form, 'msg':msg})

@permission_required('web.change_representada')
def alterar_representadas(request, representada_id):
	if request.method == 'POST':
		user_profile = UserProfile.objects.get(user=request.user)
		representada = get_object_or_404(Representada, pk=representada_id, conta_sistema=user_profile.conta_sistema)
		representada_form = RepresentadaForm(request.POST or None, instance=representada)
		if representada_form.is_valid():
			representada = representada_form.save(commit=False)
			user = User.objects.get(pk=request.user.pk)
			representada.usuario_modificacao = user
			representada.save()

			contato_representada = get_object_or_404(ContatosRepresentadas, representada=representada, conta_sistema=user_profile.conta_sistema)
			contato_representada_form = ContatoRepresentadaForm(request.POST or None, instance=contato_representada)
			if contato_representada_form.is_valid():
				contato = contato_representada_form.save(commit=False)
				contato.usuario_modificacao = user
				contato.save()

			return HttpResponseRedirect('/representadas/'+str(representada.pk)+'/?msg=2')
		else:
			representada_form = RepresentadaForm()
			print representada_form.errors
			return render(request, 'web/visualizar_representadas.html', {'user':request.user, 'class_representadas':'active', 'representada':representada, 'representada_form':representada_form})

@permission_required('web.delete_representada')
def excluir_representadas(request, representada_id):
	if request.method == 'POST':
	# try:
		get_object_or_404(Representada, pk=representada_id).delete()
		user = UserProfile.objects.get(user=request.user)
		lista_representadas = Representada.objects.filter(conta_sistema=user.conta_sistema).order_by('data_criacao')
		return HttpResponseRedirect('/representadas/?msg=1')
	# except IntegrityError as ex:
	# 	message = _("form for customer xyz was successfully updated...")
	# 	request.user.message_set.create(message = message)
	# 	return HttpResponseRedirect('/clientes/')

@login_required
def transportadoras(request):
	user = UserProfile.objects.get(user=request.user)
	lista_transportadoras = Transportadora.objects.filter(conta_sistema=user.conta_sistema).order_by('data_criacao')
	if 'msg' in request.GET: msg = request.GET['msg']
	else: msg=''
	return render(
    		request,
            'web/transportadoras.html',
            {'user':request.user, 'class_transportadoras':'active', 'lista_transportadoras': lista_transportadoras, 'msg':msg})

@permission_required('web.add_transportadora')
def cadastrar_transportadoras(request):
	if request.method == 'POST':
		transportadora_form = TransportadoraForm(data=request.POST)
		contato_transportadora_form = ContatoTransportadoraForm(data=request.POST)
		if transportadora_form.is_valid():
			transportadora = transportadora_form.save(commit=False)
			user = User.objects.get(pk=request.user.pk)
			transportadora.usuario_criacao = user
			transportadora.usuario_modificacao = user

			user_profile = UserProfile.objects.get(user=request.user)
			transportadora.conta_sistema = user_profile.conta_sistema
			transportadora.save()

			if contato_transportadora_form.is_valid():
				contato = contato_transportadora_form.save(commit=False)
				contato.conta_sistema = user_profile.conta_sistema
				contato.transportadora = transportadora
				contato.usuario_criacao = user
				contato.usuario_modificacao = user
				contato.save()

			return HttpResponseRedirect('/transportadoras/'+str(transportadora.pk)+'/?msg=1')
		else:
			print transportadora_form.errors
			print contato_transportadora_form.errors
	else:
		transportadora_form = TransportadoraForm()
		contato_transportadora_form = ContatoTransportadoraForm()
	return render(
    		request,
            'web/cadastrar_transportadoras.html',
            {'user':request.user, 'class_transportadoras':'active', 'transportadora_form':transportadora_form, 'contato_transportadora_form':contato_transportadora_form})

@login_required
def visualizar_transportadoras(request, transportadora_id):
	user_profile = UserProfile.objects.get(user=request.user)
	transportadora = get_object_or_404(Transportadora, pk=transportadora_id, conta_sistema=user_profile.conta_sistema)
	contatos_transportadoras = get_object_or_404(ContatosTransportadoras, transportadora=transportadora, conta_sistema=user_profile.conta_sistema)
	transportadora_form = TransportadoraForm()
	contato_transportadora_form = ContatoTransportadoraForm()
	if 'msg' in request.GET: msg = request.GET['msg']
	else: msg=''

	return render(
    		request,	
            'web/visualizar_transportadoras.html',
            {'user':request.user, 'class_transportadoras':'active', 'transportadora':transportadora, 'contatos_transportadoras':contatos_transportadoras, 'transportadora_form':transportadora_form, 'contato_transportadora_form':contato_transportadora_form, 'estados':ESTADOS_BRASILEIROS, 'msg':msg})

@permission_required('web.change_transportadora')
def alterar_transportadoras(request, transportadora_id):
	if request.method == 'POST':
		user_profile = UserProfile.objects.get(user=request.user)
		transportadora = get_object_or_404(Transportadora, pk=transportadora_id, conta_sistema=user_profile.conta_sistema)
		transportadora_form = TransportadoraForm(request.POST or None, instance=transportadora)
		if transportadora_form.is_valid():
			transportadora = transportadora_form.save(commit=False)
			user = User.objects.get(pk=request.user.pk)
			transportadora.usuario_modificacao = user
			transportadora.save()

			contato_transportadora = get_object_or_404(ContatosTransportadoras, transportadora=transportadora, conta_sistema=user_profile.conta_sistema)
			contato_transportadora_form = ContatoTransportadoraForm(request.POST or None, instance=contato_transportadora)
			if contato_transportadora_form.is_valid():
				contato = contato_transportadora_form.save(commit=False)
				contato.usuario_modificacao = user
				contato.save()

			return HttpResponseRedirect('/transportadoras/'+str(transportadora.pk)+'/?msg=2')
		else:
			transportadora_form = TransportadoraForm()
			print transportadora_form.errors
			return render(request, 'web/visualizar_transportadoras.html', {'user':request.user, 'class_transportadoras':'active', 'transportadora':transportadora, 'transportadora_form':transportadora_form})

@permission_required('web.delete_transportadora')
def excluir_transportadoras(request, transportadora_id):
	if request.method == 'POST':
	# try:
		get_object_or_404(Transportadora, pk=transportadora_id).delete()
		user = UserProfile.objects.get(user=request.user)
		lista_transportadoras = Transportadora.objects.filter(conta_sistema=user.conta_sistema).order_by('data_criacao')
		return HttpResponseRedirect('/transportadoras/?msg=1')
	# except IntegrityError as ex:
	# 	message = _("form for customer xyz was successfully updated...")
	# 	request.user.message_set.create(message = message)
	# 	return HttpResponseRedirect('/clientes/')

@login_required
def produtos(request):
	user = UserProfile.objects.get(user=request.user)
	lista_produtos = Produto.objects.filter(conta_sistema=user.conta_sistema).order_by('data_criacao')
	if 'msg' in request.GET: msg = request.GET['msg']
	else: msg=''
	return render(
    		request,
            'web/produtos.html',
            {'user':request.user, 'class_produtos':'active', 'lista_produtos': lista_produtos, 'msg':msg})

@permission_required('web.add_produto')
def cadastrar_produtos(request):
	if request.method == 'POST':
		produto_form = ProdutoForm(data=request.POST)
		if produto_form.is_valid():
			produto = produto_form.save(commit=False)
			user = User.objects.get(pk=request.user.pk)
			produto.usuario_criacao = user
			produto.usuario_modificacao = user

			user_profile = UserProfile.objects.get(user=request.user)
			produto.conta_sistema = user_profile.conta_sistema
			produto.representada = get_object_or_404(Representada, pk=request.POST['representada'], conta_sistema=user_profile.conta_sistema)
			produto.save()

			i = 0
			while i < len(request.POST.getlist('tamanho')):
				if len(request.POST.getlist('tamanho')) > 0:	
					tamanho_produto = TamanhoProduto(conta_sistema=user_profile.conta_sistema, produto=produto, tamanho=request.POST.getlist('tamanho')[i], usuario_criacao=user, usuario_modificacao=user)
					tamanho_produto.save()
				i = i+1

			i = 0
			while i < len(request.POST.getlist('cor')):
				# return HttpResponse('asdfasdf')
				if len(request.POST.getlist('cor')) > 0:
					cor_produto = CorProduto(conta_sistema=user_profile.conta_sistema, produto=produto, cor=request.POST.getlist('cor')[i], usuario_criacao=user, usuario_modificacao=user)
					cor_produto.save()
				i = i+1

			return HttpResponseRedirect('/produtos/'+str(produto.pk)+'/?msg=1')
		else:
			print produto_form.errors

	else:
		produto_form = ProdutoForm()

	user_profile = UserProfile.objects.get(user=request.user)
	representadas = Representada.objects.filter(conta_sistema=user_profile.conta_sistema)
	tamanhos = TamanhoProduto.objects.filter(conta_sistema=user_profile.conta_sistema).values('tamanho').distinct().order_by('tamanho')
	cores = CorProduto.objects.filter(conta_sistema=user_profile.conta_sistema).values('cor').distinct().order_by('cor')
	return render(
    		request,
            'web/cadastrar_produtos.html',
            {'user':request.user, 'class_produtos':'active', 'produto_form':produto_form, 'representadas': representadas, 'tamanhos':tamanhos, 'cores':cores})

@login_required
def visualizar_produtos(request, produto_id):
	user_profile = UserProfile.objects.get(user=request.user)
	produto = get_object_or_404(Produto, pk=produto_id, conta_sistema=user_profile.conta_sistema)
	cor_produto = CorProduto.objects.filter(produto=produto, conta_sistema=user_profile.conta_sistema)
	tamanhos = TamanhoProduto.objects.filter(conta_sistema=user_profile.conta_sistema).values_list('tamanho', flat=True).distinct().order_by('tamanho')
	cores = CorProduto.objects.filter(conta_sistema=user_profile.conta_sistema).values_list('cor', flat=True).distinct().order_by('cor')
	tamanho_produto = TamanhoProduto.objects.filter(produto=produto, conta_sistema=user_profile.conta_sistema)
	representadas = Representada.objects.filter(conta_sistema=user_profile.conta_sistema) 
	produto_form = ProdutoForm()
	if 'msg' in request.GET: msg = request.GET['msg']
	else: msg=''

	return render(
    		request,	
            'web/visualizar_produtos.html',
            {'user':request.user, 'class_produtos':'active', 'produto':produto, 'cores':cores, 'cor_produto':cor_produto, 'tamanhos':tamanhos, 'tamanho_produto':tamanho_produto, 'produto_form':produto_form, 'representadas':representadas, 'msg':msg})

@permission_required('web.change_produto')
def alterar_produtos(request, produto_id):
	if request.method == 'POST':
		user_profile = UserProfile.objects.get(user=request.user)
		produto = get_object_or_404(Produto, pk=produto_id, conta_sistema=user_profile.conta_sistema)
		produto_form = ProdutoForm(request.POST or None, instance=produto)
		if produto_form.is_valid():
			produto = produto_form.save(commit=False)
			user = User.objects.get(pk=request.user.pk)
			produto.usuario_modificacao = user

			user_profile = UserProfile.objects.get(user=request.user)
			produto.conta_sistema = user_profile.conta_sistema
			produto.representada = get_object_or_404(Representada, pk=request.POST['representada'], conta_sistema=user_profile.conta_sistema)
			produto.save()
			
			i = 0
			while i <= len(request.POST.getlist('tamanho')):
				ts = TamanhoProduto.objects.filter(conta_sistema=user_profile.conta_sistema, produto=produto).values_list('tamanho', flat=True)
				if len(ts) > 0:
					its = 0
					while its < len(ts):
						try:
						    request.POST.getlist('tamanho').index(ts[its])
						except ValueError:
							tdel = TamanhoProduto.objects.filter(conta_sistema=user_profile.conta_sistema, produto=produto, tamanho=ts[its]).delete()
						its = its+1

				if len(request.POST.getlist('tamanho')) > 0:
					try:
						t = TamanhoProduto.objects.get_or_create(conta_sistema=user_profile.conta_sistema, produto=produto, tamanho=request.POST.getlist('tamanho')[i], defaults={'usuario_modificacao': user})
					except IndexError:
						t = None
				i = i+1

			i = 0
			while i <= len(request.POST.getlist('cor')):
				cs = CorProduto.objects.filter(conta_sistema=user_profile.conta_sistema, produto=produto).values_list('cor', flat=True)
				if len(ts) > 0:
					ics = 0
					while ics < len(cs):
						try:
						    request.POST.getlist('cor').index(cs[ics])
						except ValueError:
							cdel = CorProduto.objects.filter(conta_sistema=user_profile.conta_sistema, produto=produto, cor=cs[ics]).delete()
						ics = ics+1

				if len(request.POST.getlist('cor')) > 0:
					try:
						c = CorProduto.objects.get_or_create(conta_sistema=user_profile.conta_sistema, produto=produto, cor=request.POST.getlist('cor')[i], defaults={'usuario_modificacao': user})
					except IndexError:
						c = None
				i = i+1

			return HttpResponseRedirect('/produtos/'+str(produto.pk)+'/?msg=2')
		else:
			produto_form = ClienteForm()
			print produto_form.errors
			return render(request, 'web/visualizar_produtos.html', {'user':request.user, 'class_produtos':'active', 'produto':produto, 'produto_form':produto_form})

@permission_required('web.delete_produto')
def excluir_produtos(request, produto_id):
	if request.method == 'POST':
	# try:
		get_object_or_404(Produto, pk=produto_id).delete()
		user = UserProfile.objects.get(user=request.user)
		lista_produtos = Produto.objects.filter(conta_sistema=user.conta_sistema).order_by('data_criacao')
		return HttpResponseRedirect('/produtos/?msg=1')
	# except IntegrityError as ex:
	# 	message = _("form for customer xyz was successfully updated...")
	# 	request.user.message_set.create(message = message)
	# 	return HttpResponseRedirect('/clientes/')

@login_required
def pedidos(request):
	user = UserProfile.objects.get(user=request.user)
	lista_pedidos = Pedido.objects.filter(conta_sistema=user.conta_sistema).order_by('data_criacao')
	if 'msg' in request.GET: msg = request.GET['msg']
	else: msg=''
	return render(
    		request,
            'web/pedidos.html',
            {'user':request.user, 'class_pedidos':'active', 'lista_pedidos': lista_pedidos, 'msg':msg})

@permission_required('web.add_pedido')
def cadastrar_pedidos(request):
	val={}
	produto={}
	if request.method == 'POST':
		pedido_form = PedidoForm(data=request.POST)
		if pedido_form.is_valid():

			pedido = pedido_form.save(commit=False)
			user = User.objects.get(pk=request.user.pk)
			user_profile = UserProfile.objects.get(user=request.user)
			pedido.conta_sistema = user_profile.conta_sistema
			pedido.cliente = Cliente.objects.get(pk=request.POST['cliente'])
			pedido.representada = Representada.objects.get(pk=request.POST['representada'])
			pedido.numero_pedido = request.POST['numero_pedido']
			pedido.vendedor = UserProfile.objects.get(pk=request.POST['vendedor'])
			if request.POST.get('transportadora',False)!=False: pedido.transportadora = Transportadora.objects.get(pk=request.POST.get('transportadora', False))
			pedido.contato_cliente = request.POST['contato_cliente']
			pedido.usuario_criacao = user
			pedido.usuario_modificacao = user
			pedido.save()

			i = 0

			while i < len(request.POST.getlist('id_produto')):
				if len(request.POST.getlist('id_produto')) > 0:	
					# produto_pedido = ProdutosPedidos(conta_sistema=user_profile.conta_sistema, produto=produto, tamanho=request.POST.getlist('tamanho')[i], usuario_criacao=user, usuario_modificacao=user)
					produto_pedido = ProdutosPedidos()
					produto_pedido.conta_sistema = user_profile.conta_sistema
					produto_pedido.pedido = Pedido.objects.get(pk=pedido.pk)
					produto_pedido.produto = Produto.objects.get(pk=request.POST.getlist('id_produto')[i])
					produto_pedido.quantidade = request.POST.getlist('qtd_produto')[i]
					produto_pedido.tabela_preco = request.POST.getlist('preco_tabela')[i]
					produto_pedido.tipo_preco = request.POST.getlist('tipo_preco')[i]
					produto_pedido.desconto = request.POST.getlist('desconto')[i]
					produto_pedido.preco_liquido = request.POST.getlist('preco_liquido')[i]
					produto_pedido.observacoes = request.POST.getlist('observacoes_produto')[i]
					produto_pedido.save()
				i = i+1

			return HttpResponseRedirect('/pedidos/'+str(pedido.pk)+'/?msg=1')
		else:
			print pedido_form.errors
			val = {
			'cliente': request.POST.get('cliente','n'),
			'representada': request.POST.get('representada','n'),
			'numero_pedido': request.POST.get('numero_pedido','n'),
			'vendedor': request.POST.get('vendedor','n'),
			'transportadora': request.POST.get('transportadora','n'),
			'contato_cliente': request.POST.get('contato_cliente','n'),
			'produto': request.POST.getlist('id_produto'),
			'descricao': request.POST.getlist('descricao'),
			'quantidade': request.POST.getlist('qtd_produto'),
			'tabela_preco': request.POST.getlist('preco_tabela'),
			'tipo_preco': request.POST.getlist('tipo_preco'),
			'desconto': request.POST.getlist('desconto'),
			'preco_liquido': request.POST.getlist('preco_liquido'),
			'subtotal': request.POST.getlist('subtotal'),
			'observacoes_produto': request.POST.getlist('observacoes_produto'),
			}
	else:
		pedido_form = PedidoForm()

	user_profile = UserProfile.objects.get(user=request.user)
	representadas = Representada.objects.filter(conta_sistema=user_profile.conta_sistema)
	clientes = Cliente.objects.filter(conta_sistema=user_profile.conta_sistema)
	vendedores = UserProfile.objects.filter(conta_sistema=user_profile.conta_sistema)
	transportadoras = Transportadora.objects.filter(conta_sistema=user_profile.conta_sistema)
	try:
		numero_pedido = Pedido.objects.filter(conta_sistema=user_profile.conta_sistema).order_by('-numero_pedido')[0]
		numero_pedido = int(numero_pedido.numero_pedido) + 1
	except IndexError:
		numero_pedido = 1

	produtos_pedidos_form = ProdutosPedidosForm()
	return render(
    		request,
            'web/cadastrar_pedidos.html',
            {'val':val, 'user':request.user, 'class_pedidos':'active', 'pedido_form':pedido_form, 'produtos_pedidos_form':produtos_pedidos_form, 'representadas':representadas, 'clientes':clientes, 'vendedores':vendedores, 'transportadoras':transportadoras, 'numero_pedido': numero_pedido})

@permission_required('web.add_pedido')
def lista_contatos_cliente(request, contato_id):
	user_profile = UserProfile.objects.get(user=request.user)
	cliente = Cliente.objects.get(pk=contato_id)
	contatos_clientes = ContatosClientes.objects.filter(conta_sistema=user_profile.conta_sistema, cliente=cliente)
	lista_contatos_cliente = serializers.serialize("json", contatos_clientes)
	return HttpResponse(lista_contatos_cliente)

@permission_required('web.add_pedido')
def lista_produtos_representada(request, representada_id):
	user = UserProfile.objects.get(user=request.user)
	lista_produtos = Produto.objects.filter(conta_sistema=user.conta_sistema, representada=representada_id).order_by('data_criacao')
	return render(
    		request,
            'web/modal/addProduto.html',
            {'lista_produtos': lista_produtos})

@permission_required('web.add_pedido')
def lista_produtos_representada_editar(request, representada_id):
	user = UserProfile.objects.get(user=request.user)
	lista_produtos = Produto.objects.filter(conta_sistema=user.conta_sistema, representada=representada_id).order_by('data_criacao')
	return render(
    		request,
            'web/modal/editarProduto.html',
            {'lista_produtos': lista_produtos})

@permission_required('web.add_pedido')
def lista_tabela_preco_produto(request, produto_id):
	user_profile = UserProfile.objects.get(user=request.user)
	produto = Produto.objects.filter(conta_sistema=user_profile.conta_sistema, pk=produto_id)
	lista_tabela_preco_produto = serializers.serialize("json", produto)
	return HttpResponse(lista_tabela_preco_produto)

@login_required
def visualizar_pedidos(request, pedido_id):
	user_profile = UserProfile.objects.get(user=request.user)
	pedido = get_object_or_404(Pedido, pk=pedido_id, conta_sistema=user_profile.conta_sistema)
	clientes = Cliente.objects.filter(conta_sistema=user_profile.conta_sistema)
	representadas = Representada.objects.filter(conta_sistema=user_profile.conta_sistema)
	vendedores = UserProfile.objects.filter(conta_sistema=user_profile.conta_sistema)
	transportadoras = Transportadora.objects.filter(conta_sistema=user_profile.conta_sistema)
	produto_pedido = ProdutosPedidos.objects.filter(conta_sistema=user_profile.conta_sistema, pedido=pedido)
	# pedido_form = PedidoForm()
	if 'msg' in request.GET: msg = request.GET['msg']
	else: msg=''

	return render(
    		request,	
            'web/visualizar_pedidos.html',
            {'user':request.user, 'class_pedidos':'active', 'pedido':pedido, 'clientes':clientes, 'representadas':representadas, 'vendedores':vendedores, 'transportadoras':transportadoras, 'produto_pedido':produto_pedido, 'msg':msg})

@permission_required('web.change_pedido')
def alterar_pedidos(request, pedido_id):
	if request.method == 'POST':
		user_profile = UserProfile.objects.get(user=request.user)
		pedido = get_object_or_404(Pedido, pk=pedido_id, conta_sistema=user_profile.conta_sistema)
		pedido_form = PedidoForm(request.POST or None, instance=pedido)
		if pedido_form.is_valid():
			pedido = pedido_form.save(commit=False)
			user = User.objects.get(pk=request.user.pk)
			user_profile = UserProfile.objects.get(user=request.user)
			pedido.conta_sistema = user_profile.conta_sistema
			pedido.cliente = get_object_or_404(Cliente, pk=request.POST['cliente'], conta_sistema=user_profile.conta_sistema)
			pedido.representada = get_object_or_404(Representada, pk=request.POST['representada'], conta_sistema=user_profile.conta_sistema)
			pedido.numero_pedido = request.POST.get('numero_pedido',False)
			pedido.vendedor = UserProfile.objects.get(pk=request.POST.get('vendedor',False))
			if request.POST.get('transportadora',False)!=False: pedido.transportadora = Transportadora.objects.get(pk=request.POST.get('transportadora', False))
			pedido.contato_cliente = request.POST.get('contato_cliente',False)
			pedido.usuario_modificacao = user
			pedido.save()

			i = 0
			while i < len(request.POST.getlist('id_produto')):
				if len(request.POST.getlist('id_produto')) > 0:	
					produto_pedido = get_object_or_404(ProdutosPedidos, pk=request.POST.getlist('id_produto_pedido')[i], conta_sistema=user_profile.conta_sistema)
					produto_pedido.conta_sistema = user_profile.conta_sistema
					produto_pedido.pedido = Pedido.objects.get(pk=pedido.pk)
					produto_pedido.produto = Produto.objects.get(pk=request.POST.getlist('id_produto')[i])
					produto_pedido.quantidade = request.POST.getlist('qtd_produto')[i]
					produto_pedido.tabela_preco = request.POST.getlist('preco_tabela')[i]
					produto_pedido.tipo_preco = request.POST.getlist('tipo_preco')[i]
					produto_pedido.desconto = request.POST.getlist('desconto')[i]
					produto_pedido.preco_liquido = request.POST.getlist('preco_liquido')[i]
					produto_pedido.observacoes = request.POST.getlist('observacoes_produto')[i]
					produto_pedido.save()
				i = i+1


			return HttpResponseRedirect('/pedidos/'+str(pedido.pk)+'/?msg=2')
		else:
			pedido_form = PedidoForm()
			print pedido_form.errors
			return render(request, 'web/visualizar_pedidos.html', {'user':request.user, 'class_pedidos':'active', 'pedido':pedido, 'pedido_form':pedido_form})

@permission_required('web.delete_pedido')
def excluir_pedidos(request, pedido_id):
	if request.method == 'POST':
	# try:
		get_object_or_404(Pedido, pk=pedido_id).delete()
		user = UserProfile.objects.get(user=request.user)
		lista_pedidos = Pedido.objects.filter(conta_sistema=user.conta_sistema).order_by('data_criacao')
		return HttpResponseRedirect('/pedidos/?msg=1')

	# except IntegrityError as ex:
	# 	message = _("form for customer xyz was successfully updated...")
	# 	request.user.message_set.create(message = message)
	# 	return HttpResponseRedirect('/clientes/')

@login_required
def agenda(request):
	user = UserProfile.objects.get(user=request.user)
	return render(
    		request,
            'web/agenda.html',
            {'user':request.user, 'class_agenda':'active'})

@permission_required('web.add_agenda')
def cadastrar_agenda(request):
	val = {}
	if request.method == 'POST':
		agenda_form = AgendaForm(data=request.POST)
		if agenda_form.is_valid():
			agenda = agenda_form.save(commit=False)
			agenda.responsavel = UserProfile.objects.get(pk=request.POST.get('responsavel',False))
			agenda.start = request.POST.get('start', False)
			user = User.objects.get(pk=request.user.pk)
			agenda.usuario_criacao = user
			agenda.usuario_modificacao = user

			user_profile = UserProfile.objects.get(user=request.user)
			agenda.conta_sistema = user_profile.conta_sistema
			agenda.save()

			# return HttpResponseRedirect('/agenda/'+str(agenda.pk)+'/?msg=1')
			return HttpResponse('ok')
		else:
			print agenda_form.errors
			val = {
			'responsavel': request.POST.get('responsavel','n'),
			}

	else:
		agenda_form = AgendaForm()

	user = UserProfile.objects.get(user=request.user)
	user_profile = UserProfile.objects.get(user=request.user)
	responsavel = UserProfile.objects.filter(conta_sistema=user_profile.conta_sistema)
	return render(
    		request,
            'web/cadastrar_agenda.html',
            {'user':request.user, 'class_agenda':'active', 'agenda_form':agenda_form, 'responsavel':responsavel, 'val':val})

@login_required
def usuarios(request):
	user = UserProfile.objects.get(user=request.user)
	user_profile = UserProfile.objects.get(user=request.user)
	lista_usuarios = UserProfile.objects.filter(conta_sistema=user.conta_sistema)
	return render(
    		request,
            'web/usuarios.html',
            {'user':request.user, 'class_configuracoes':'active', 'lista_usuarios': lista_usuarios})

def gera_senha():
    caracters = '0123456789'
    senha = ''
    for char in xrange(6):
            senha += choice(caracters)
    return  senha
	    

@permission_required('web.add_usuario')
def cadastrar_usuarios(request):
    if request.method == 'POST':
    	perms = {}
    	val = {}
        usuario_form = UsuarioForm(data=request.POST)
        user_profile_form = UserProfileForm(request.POST, request.FILES)
        if usuario_form.is_valid():

        	email = request.POST.get('username','')
        	senha = gera_senha()

        	usuario = User.objects.create_user(email, email, senha)
        	usuario.first_name = request.POST.get('first_name','')
        	usuario.last_name = request.POST.get('last_name','')
        	usuario.save()

        	user_profile = UserProfile.objects.get(user=request.user)

        	profile = UserProfile()
        	profile.user = User.objects.get(pk=usuario.pk)
        	profile.conta_sistema = user_profile.conta_sistema
        	profile.first_name = request.POST.get('first_name','')
        	profile.last_name = request.POST.get('last_name','')
        	profile.telefone = request.POST.get('telefone', '')
        	profile.picture = request.FILES.get('picture', '')
        	profile.assinatura_email = request.POST.get('assinatura_email', '')
        	profile.save()

        	user = User.objects.get(pk=request.user.pk)

        	for cli in request.POST.getlist('cliente_usuario'):
        		cliente = Cliente.objects.get(pk=cli)

        		cliente_vendedor = ClientesVendedor()
        		cliente_vendedor.conta_sistema = user_profile.conta_sistema
        		cliente_vendedor.vendedor = profile
        		cliente_vendedor.cliente = cliente
        		cliente_vendedor.usuario_criacao = user
        		cliente_vendedor.usuario_modificacao = user
        		cliente_vendedor.save()

        	for rep in request.POST.getlist('id_representada_usuario'):
        		representada = Representada.objects.get(pk=rep)

        		representada_vendedor = RepresentadasVendedor()
        		representada_vendedor.conta_sistema = user_profile.conta_sistema
        		representada_vendedor.vendedor = profile
        		representada_vendedor.representada = representada
        		representada_vendedor.comissao = 5
        		representada_vendedor.usuario_criacao = user
        		representada_vendedor.usuario_modificacao = user
        		representada_vendedor.save()

        	user = User.objects.get(pk=request.user.pk)
        	msg_html = render_to_string('web/email.html', {'email': email, 'senha':senha, 'usuario':user.first_name, 'empresa':user_profile.conta_sistema})

        	usuario.user_permissions.clear()
        	
	    	for key in request.POST:
	    		value = request.POST[key]
			for key, value in request.POST.iteritems():
				if 'can_' in key:
					nome = key.capitalize().replace('_',' ')
					permission = Permission.objects.get(name=nome)
					usuario.user_permissions.add(permission)

        	# if send_mail('Dados de Acesso E-pedidos', '', 'e-pedidos@e-pedidos.com', ['flavio@sacavalcante.com.br'], html_message=msg_html) == 0:
        	# 	return HttpResponse('Ocorreu um erro ao enviar o e-mail para ' + email + ' com os dados de acesso.')

        	return HttpResponseRedirect('/usuarios/'+str(usuario.pk)+'/?msg=1')

        else:
            print usuario_form.errors
            print user_profile_form.errors
            val = {
            'assinatura_email': request.POST.get('assinatura_email', ''),
            'id_representada_usuario': request.POST.getlist('id_representada_usuario'),
            'representada_usuario_comissao': request.POST.getlist('representada_usuario_comissao'),
            'cliente_usuario': request.POST.getlist('cliente_usuario'),
            'cliente_usuario_total': request.POST.getlist('cliente_usuario_total')
            }
            perms = {
			'can_view_agenda': request.POST.get('can_view_agenda'),
			'can_add_agenda': request.POST.get('can_add_agenda'),
			'can_change_agenda': request.POST.get('can_change_agenda'),
			'can_delete_agenda': request.POST.get('can_delete_agenda'),
			'can_self_agenda': request.POST.get('can_self_agenda'),

			'can_view_cliente': request.POST.get('can_view_cliente'),
			'can_add_cliente': request.POST.get('can_add_cliente'),
			'can_change_cliente': request.POST.get('can_change_cliente'),
			'can_delete_cliente': request.POST.get('can_delete_cliente'),
			'can_self_cliente': request.POST.get('can_self_cliente'),
			
			'can_view_pedido': request.POST.get('can_view_pedido'),
			'can_add_pedido': request.POST.get('can_add_pedido'),
			'can_change_pedido': request.POST.get('can_change_pedido'),
			'can_delete_pedido': request.POST.get('can_delete_pedido'),
			'can_self_pedido': request.POST.get('can_self_pedido'),

			'can_view_produto': request.POST.get('can_view_produto'),
			'can_add_produto': request.POST.get('can_add_produto'),
			'can_change_produto': request.POST.get('can_change_produto'),
			'can_delete_produto': request.POST.get('can_delete_produto'),
			'can_self_produto': request.POST.get('can_self_produto'),

			'can_view_representada': request.POST.get('can_view_representada'),
			'can_add_representada': request.POST.get('can_add_representada'),
			'can_change_representada': request.POST.get('can_change_representada'),
			'can_delete_representada': request.POST.get('can_delete_representada'),

			'can_view_transportadora': request.POST.get('can_view_transportadora'),
			'can_add_transportadora': request.POST.get('can_add_transportadora'),
			'can_change_transportadora': request.POST.get('can_change_transportadora'),
			'can_delete_transportadora': request.POST.get('can_delete_transportadora'),

			'can_view_usuario': request.POST.get('can_view_usuario'),
			'can_add_usuario': request.POST.get('can_add_usuario'),
			'can_change_usuario': request.POST.get('can_change_usuario'),
			'can_delete_usuario': request.POST.get('can_delete_usuario'),
			}

    else:
    	perms = {}
    	val = {}
        usuario_form = UsuarioForm()
        user_profile_form = UserProfileForm()
        
    user_profile = UserProfile.objects.get(user=request.user)
    clientes = Cliente.objects.filter(conta_sistema=user_profile.conta_sistema)
    representadas = Representada.objects.filter(conta_sistema=user_profile.conta_sistema)
    return render(
    		request,
            'web/cadastrar_usuarios.html',
            {'user':request.user, 'class_configuracoes':'active', 'usuario_form': usuario_form, 'user_profile_form': user_profile_form, 'clientes': clientes, 'representadas': representadas, 'perms': perms, 'val': val})

@login_required
def visualizar_usuarios(request, usuario_id):
	usuario = User.objects.get(pk=usuario_id)
	user_profile = UserProfile.objects.get(user=usuario_id)
	representadas = Representada.objects.filter(conta_sistema=user_profile.conta_sistema)
	representadas_vendedor = RepresentadasVendedor.objects.filter(conta_sistema=user_profile.conta_sistema, vendedor=user_profile)
	clientes = Cliente.objects.filter(conta_sistema=user_profile.conta_sistema)
	clientes_vendedor = ClientesVendedor.objects.filter(conta_sistema=user_profile.conta_sistema, vendedor=user_profile)
	permissoes = Permission.objects.filter(user=usuario_id)
	# contatos_clientes = get_object_or_404(ContatosClientes, cliente=cliente, conta_sistema=user_profile.conta_sistema)
	# cliente_form = ClienteForm()
	# contato_cliente_form = ContatoClienteForm()
	if 'msg' in request.GET: msg = request.GET['msg']
	else: msg=''

	return render(
    		request,	
            'web/visualizar_usuarios.html',
            {'user':request.user, 'class_configuracoes':'active', 'usuario': usuario, 'user_profile': user_profile, 'representadas': representadas, 'representadas_vendedor': representadas_vendedor, 'clientes': clientes, 'clientes_vendedor': clientes_vendedor, 'permissoes': permissoes, 'msg':msg})

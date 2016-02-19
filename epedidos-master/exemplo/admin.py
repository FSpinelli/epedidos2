from django.contrib import admin
from django.contrib.auth.models import Permission
from web.models import *

admin.site.register(Permission)
admin.site.register(ContaSistema)
admin.site.register(UserProfile)
admin.site.register(ContatosClientes)
admin.site.register(Cliente)
admin.site.register(ContatosRepresentadas)
admin.site.register(Representada)
admin.site.register(ContatosTransportadoras)
admin.site.register(Transportadora)
admin.site.register(TamanhoProduto)
admin.site.register(CorProduto)
admin.site.register(Produto)
admin.site.register(Pedido)
admin.site.register(ProdutosPedidos)
admin.site.register(Agenda)
admin.site.register(RepresentadasVendedor)
admin.site.register(ClientesVendedor)

# class ClienteAdmin(admin.ModelAdmin):
#     list_display = ('conta_sistema', 'razao_social_ou_nome', 'nome_fantasia', 'tipo_pessoa', 'cnpj', 'cpf', 'telefone', 'email', 'inscricao_estadual')

# admin.site.register(Cliente, ClienteAdmin)
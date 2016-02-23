from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^cadastrar/', views.cadastrar, name='cadastrar'),
    url(r'^login/', views.login, name='login'),
]
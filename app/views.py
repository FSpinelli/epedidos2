from django.http import HttpResponse
from django.template import loader

from .models import *


def index(request):
    template = loader.get_template('app/index.html')
    return HttpResponse(template.render(request))
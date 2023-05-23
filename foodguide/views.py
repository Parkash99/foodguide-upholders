from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.template import loader
from django.urls import reverse

def view_login(request):
    template = loader.get_template('login.html')
    context = {
        'login_page': 'login',
    }
    return HttpResponse(template.render(context, request))

def view_index(request):
    template = loader.get_template('index.html')
    context = {
        'index_page': 'index',
    }
    return HttpResponse(template.render(context, request))
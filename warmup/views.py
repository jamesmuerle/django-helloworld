# Create your views here.
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import simplejson
from warmup.models import UsersModel

# /
def index(request):
    context = {}
    return render(request, 'warmup/index.html', context)


# /users/login
def login(request):
    r_user = request.POST['user']
    r_pass = request.POST['password']
    json_data = UsersModel.login(user=r_user, password=r_pass)
    return HttpResponse(json_data, mimetype='application/json')


# /users/add
def add(request):
    r_user = request.POST['user']
    r_pass = request.POST['password']
    json_data = UsersModel.add(user=r_user, password=r_pass)
    return HttpResponse(json_data, mimetype='application/json')


# /TESTAPI/resetFixture
def TESTAPI_resetfixture(request):
    json_data = UsersModel.TESTAPI_resetfixture()
    return HttpResponse(json_data, mimetype='application/json')


# /TESTAPI/unitTests
def TESTAPI_unittests(request):
    data = {
        'totalTests': 1,
        'nrFailed': 1,
        'output': 'text',
    }

    json_data = simplejson.dumps(data)
    return HttpResponse(json_data, mimetype='application/json')
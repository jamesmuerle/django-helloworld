# Create your views here.
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import simplejson
from warmup.models import UsersModel
from warmup.tests import TestUsersModel
import StringIO
import unittest
from django.views.decorators.csrf import csrf_exempt

# /
@csrf_exempt
def index(request):
    context = {}
    return render(request, 'warmup/index.html', context)


# /users/login
@csrf_exempt
def login(request):
    request_data = simplejson.loads(request.body)
    r_user = request_data['user']
    r_pass = request_data['password']
    json_data = UsersModel.login(user=r_user, password=r_pass)
    return HttpResponse(json_data, content_type='application/json')


# /users/add
@csrf_exempt
def add(request):
    request_data = simplejson.loads(request.body)
    r_user = request_data['user']
    r_pass = request_data['password']
    json_data = UsersModel.add(user=r_user, password=r_pass)
    return HttpResponse(json_data, content_type='application/json')


# /TESTAPI/resetFixture
@csrf_exempt
def TESTAPI_resetfixture(request):
    json_data = UsersModel.TESTAPI_resetfixture()
    return HttpResponse(json_data, content_type='application/json')


# /TESTAPI/unitTests
@csrf_exempt
def TESTAPI_unittests(request):
    buffer = StringIO.StringIO()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestUsersModel)
    result = unittest.TextTestRunner(stream = buffer, verbosity = 2).run(suite)

    rv = {"totalTests": result.testsRun, "nrFailed": len(result.failures), "output": buffer.getvalue()}
    return HttpResponse(simplejson.dumps(rv), content_type = "application/json")

from django.db import models
from warmup.errors import Errors
from django.utils import simplejson


# Create your models here.
class UsersModel(models.Model):

    # Database fields
    user = models.CharField(max_length=128)
    password = models.CharField(max_length=128)
    count = models.IntegerField(default=1)


    # Model actions
    def login(user, password):
        # This function checks the user/password in the database. 
        # On success, the function updates the count of logins in the database.
        # On success the result is either the number of logins (including this one) (>= 1)
        # On failure the result is an error code (< 0) from the list below:
            # ERR_BAD_CREDENTIALS
        data = {
            'errCode': Errors.ERR_BAD_CREDENTIALS
        }
        data = {
            'errCode': Errors.SUCCESS,
            'count': count, # only present on success
        }

        json_data = simplejson.dumps(data)
        return HttpResponse(json_data, mimetype='application/json')


    def add(user, password):
        # Checks the following:
        #  -user is not empty and not more than 128 characters long
        #  -password is not more than 128 characters long
        #  -user is not already existent in the database

        # If all pass, new user is added to the database and count is set to 1
        # If there's a failure, the correct error code is returned.
        pass

    # TESTAPI methods
    def TESTAPI_resetfixture():
        # Deletes all rows in the database.
        data = {
            'errCode': Errors.SUCCESS
        }

        json_data = simplejson.dumps(data)
        return HttpResponse(json_data, mimetype='application/json')


    def TESTAPI_unittests():
        data = {
            'totalTests': 1,
            'nrFailed': 1,
            'output': 'text',
        }

        json_data = simplejson.dumps(data)
        return HttpResponse(json_data, mimetype='application/json')


    # For debugging ease
    def __unicode__():
        return user + ' ' + password

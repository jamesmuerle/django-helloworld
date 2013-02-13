from django.db import models
from testLib import RestTestCase
from django.utils import simplejson


# Create your models here.
class UsersModel(models.Model):

    # Database fields
    u_user = models.CharField(max_length=128)
    u_password = models.CharField(max_length=128)
    u_count = models.IntegerField(default=1)


    # Model actions
    @staticmethod
    def login(user, password):
        # This function checks the user/password in the database. 
        # On success, the function updates the count of logins in the database.
        # On success the result is either the number of logins (including this one) (>= 1)
        # On failure the result is an error code (< 0) from the list below:
            # ERR_BAD_CREDENTIALS
        results = UsersModel.objects.filter(u_user=user, u_password=password)
        if len(results) == 1:
            results[0].u_count = results[0].u_count + 1
            results[0].save()
            count = results[0].u_count
            data = {
                'errCode': RestTestCase.SUCCESS,
                'count': count, # only present on success
            }
        else:
            data = {
                'errCode': RestTestCase.ERR_BAD_CREDENTIALS,
            }

        json_data = simplejson.dumps(data)
        return json_data


    @staticmethod
    def add(user, password):
        # Checks the following:
        #  -user is not empty and not more than 128 characters long
        #  -password is not more than 128 characters long
        #  -user is not already existent in the database

        # If all pass, new user is added to the database and count is set to 1
        # If there's a failure, the correct error code is returned.
        user_len = len(user)
        pass_len = len(password)
        if user_len <= 0 or user_len > 128:
            data = {
                'errCode': RestTestCase.ERR_BAD_USERNAME,
            }
        elif pass_len > 128:
            data = {
                'errCode': RestTestCase.ERR_BAD_PASSWORD,
            }
        elif len(UsersModel.objects.filter(u_user=user)) > 0:
            data = {
                'errCode': RestTestCase.ERR_USER_EXISTS,
            }
        else:
            u = UsersModel(u_user=user, u_password=password)
            u.save()
            data = {
                'errCode': RestTestCase.SUCCESS,
                'count': u.u_count,
            }

        json_data = simplejson.dumps(data)
        return json_data


    # TESTAPI methods
    @staticmethod
    def TESTAPI_resetfixture():
        # Deletes all rows in the database.
        for user_instance in UsersModel.objects.all():
            user_instance.delete()

        data = {
            'errCode': RestTestCase.SUCCESS
        }

        json_data = simplejson.dumps(data)
        return json_data


    # For debugging ease
    def __unicode__(self):
        return 'USERNAME:' + self.u_user + ', PASSWORD:' + self.u_password + ', COUNT:' + str(self.u_count)

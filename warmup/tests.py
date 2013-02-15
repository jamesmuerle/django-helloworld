import unittest
import testLib
# from testAdditional import TestResponse
import os
os.environ["DJANGO_SETTINGS_MODULE"] = "hellodjango.settings"
from warmup.models import UsersModel
import json

# Class that is a little different from the one in testAdditional.py because it doesn't extend RestTestCase
class TestResponse(unittest.TestCase):
    def assertResponse(self, respData, count = 1, errCode = testLib.RestTestCase.SUCCESS):
        """
        Check that the response data dictionary matches the expected values
        """
        respData = json.loads(respData)
        expected = { 'errCode' : errCode }
        if count is not None:
            expected['count']  = count
        self.assertDictEqual(expected, respData)

# Unit test that tests the UsersModel class
class TestUsersModel(TestResponse):
    # Make sure login succeeds after adding.
    def testLoginJames(self):
        UsersModel.TESTAPI_resetfixture()
        UsersModel.add('james', 'muerle')
        respData = UsersModel.login('james', 'muerle')

        self.assertResponse(respData, count = 2)


    # Make sure logging in multiple times increments the count.
    def testLoginSequence(self):
        UsersModel.TESTAPI_resetfixture()
        UsersModel.add('james', 'muerle')
        respData = UsersModel.login('james', 'muerle')
        self.assertResponse(respData, count = 2)
        respData = UsersModel.login('james', 'muerle')
        self.assertResponse(respData, count = 3)
        respData = UsersModel.login('james', 'muerle')
        self.assertResponse(respData, count = 4)


    # Make sure adding a second user doesn't screw with the rest of the rows.
    def testLoginJames2(self):
        UsersModel.TESTAPI_resetfixture()
        UsersModel.add('james', 'muerle')
        UsersModel.login('james', 'muerle')
        UsersModel.login('james', 'muerle')
        UsersModel.login('james', 'muerle')
        UsersModel.login('james', 'muerle')

        UsersModel.add('james2', 'muerle')
        respData = UsersModel.login('james2', 'muerle')
        self.assertResponse(respData, count = 2)

        respData = UsersModel.login('james', 'muerle')
        self.assertResponse(respData, count = 6)


    # Make sure logging with incorrect username errors.
    def testLoginIncorrectUsername(self):
        UsersModel.TESTAPI_resetfixture()
        UsersModel.add('james', 'muerle')
        respData = UsersModel.login('notjames', 'muerle')
        self.assertResponse(respData, count = None, errCode = testLib.RestTestCase.ERR_BAD_CREDENTIALS)
        

    # Make sure logging with incorrect password errors.
    def testLoginIncorrectPassword(self):
        UsersModel.TESTAPI_resetfixture()
        UsersModel.add('james', 'muerle')
        respData = UsersModel.login('james', 'notmuerle')
        self.assertResponse(respData, count = None, errCode = testLib.RestTestCase.ERR_BAD_CREDENTIALS)


    # Make sure users are added to the database.
    def testAddTwoPeople(self):
        UsersModel.TESTAPI_resetfixture()
        UsersModel.add('james1', 'muerle')
        self.assertEqual(len(UsersModel.objects.all()), 1)
        UsersModel.add('james2', 'muerle')
        self.assertEqual(len(UsersModel.objects.all()), 2)


    # Make sure adding a user that exists gives an error.
    def testAddExistingUser(self):
        UsersModel.TESTAPI_resetfixture()
        UsersModel.add('james', 'muerle')

        respData = UsersModel.add('james', 'some_password')
        self.assertResponse(respData, count = None, errCode = testLib.RestTestCase.ERR_USER_EXISTS)


    # Make sure passwords can't be too long.
    def testAddLongPassword(self):
        UsersModel.TESTAPI_resetfixture()
        respData = UsersModel.add('notjames', 'somereallylongpasswordthatismorethan128asciicharacterslonginlengthsomereallylongpasswordthatismorethan128asciicharacterslonginlength')
        self.assertResponse(respData, count = None, errCode = testLib.RestTestCase.ERR_BAD_PASSWORD)


    # Make sure usernames can't be too long.
    def testAddLongUsername(self):
        UsersModel.TESTAPI_resetfixture()
        respData = UsersModel.add('somereallylongusernamethatismorethan128asciicharacterslonginlengthsomereallylongusernamethatismorethan128asciicharacterslonginlength', 'muerle')
        self.assertResponse(respData, count = None, errCode = testLib.RestTestCase.ERR_BAD_USERNAME)


    # Make sure usernames can't be empty.
    def testAddEmptyUsername(self):
        UsersModel.TESTAPI_resetfixture()
        respData = UsersModel.add('', 'muerle')
        self.assertResponse(respData, count = None, errCode = testLib.RestTestCase.ERR_BAD_USERNAME)


    # Unit test that tests the resetFixture function in UsersModel
    def testResetFixture(self):
        UsersModel.TESTAPI_resetfixture()
        UsersModel.add('james', 'muerle')
        self.assertEqual(len(UsersModel.objects.all()), 1)
        UsersModel.TESTAPI_resetfixture()
        self.assertEqual(len(UsersModel.objects.all()), 0)

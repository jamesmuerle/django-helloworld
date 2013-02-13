import unittest
import testLib
from warmup.models import UsersModel

# Class with assertResponse so I don't have to write it a bunch.
class TestResponse(testLib.RestTestCase)
    def assertResponse(self, respData, count = 1, errCode = testLib.RestTestCase.SUCCESS):
        """
        Check that the response data dictionary matches the expected values
        """
        expected = { 'errCode' : errCode }
        if count is not None:
            expected['count']  = count
        self.assertDictEqual(expected, respData)


# Unit test that tests the login function in UsersModel
class TestLogin(TestResponse):
    # Make sure login succeeds after adding.
    def testLogin1():
        self.makeRequest("/TESTAPI/resetfixture")
        self.makeRequest("/users/add", method="POST", data = {'user': 'james', 'password': 'muerle'})
        respData = self.makeRequest("/users/login", method="POST", data = {'user': 'james', 'password': 'muerle'})
        self.assertResponse(respData)

    # Make sure logging in multiple times increments the count.
    def testLogin2():
        # second login
        respData = self.makeRequest("/users/login", method="POST", data = {'user': 'james', 'password': 'muerle'})
        self.assertResponse(respData, count = 2)
        # third login
        respData = self.makeRequest("/users/login", method="POST", data = {'user': 'james', 'password': 'muerle'})
        self.assertResponse(respData, count = 3)
        # fourth login
        respData = self.makeRequest("/users/login", method="POST", data = {'user': 'james', 'password': 'muerle'})
        self.assertResponse(respData, count = 4)

    # Make sure adding a second user doesn't screw with the rest of the rows.
    def testLogin3():
        self.makeRequest("/users/add", method="POST", data = {'user': 'james2', 'password': 'muerle'})
        respData = self.makeRequest("/users/login", method="POST", data = {'user': 'james2', 'password': 'muerle'})
        # Checks new user's count to be 1
        self.assertResponse(respData)
        # Checks old user's count to still be 4
        self.assertEqual(UsersModel.objects.filter(u_uname = 'james')[0].u_count, 4)


    # Make sure logging with incorrect username errors.
    def testLogin4():
        respData = self.makeRequest("/users/login", method="POST", data = {'user': 'notjames', 'password': 'muerle'})
        self.assertResponse(respData, count = None, errCode = testLib.RestTestCase.ERR_BAD_CREDENTIALS)

    # Make sure logging with incorrect password errors.
    def testLogin5():
        respData = self.makeRequest("/users/login", method="POST", data = {'user': 'james', 'password': 'notmuerle'})
        self.assertResponse(respData, count = None, errCode = testLib.RestTestCase.ERR_BAD_CREDENTIALS)


# Unit test that tests the add function in UsersModel
class TestAdd(TestResponse):
    # Make sure users are added to the database.
    def testAdd1():
        self.makeRequest("/TESTAPI/resetfixture")
        self.makeRequest("/users/add", method="POST", data = {'user': 'james1', 'password': 'muerle'})
        self.assertEqual(len(UsersModel.objects.all()), 1)
        self.makeRequest("/users/add", method="POST", data = {'user': 'james2', 'password': 'muerle'})
        self.assertEqual(len(UsersModel.objects.all()), 2)

    # Make sure adding a user that exists gives an error.
    def testAdd2():
        respData = self.makeRequest("/users/add", method="POST", data = {'user': 'james', 'password': 'some_password'})
        self.assertResponse(respData, count = None, errCode = testLib.RestTestCase.ERR_USER_EXISTS)

    # Make sure passwords can't be too long.
    def testAdd3():
        respData = self.makeRequest("/users/add", method="POST", data = {'user': 'notjames', 'password': 'somereallylongpasswordthatismorethan128asciicharacterslonginlengthsomereallylongpasswordthatismorethan128asciicharacterslonginlength'})
        self.assertResponse(respData, count = None, errCode = testLib.RestTestCase.ERR_BAD_PASSWORD)

    # Make sure usernames can't be too long nor empty.
    def testAdd4():
        respData = self.makeRequest("/users/add", method="POST", data = {'user': 'somereallylongusernamethatismorethan128asciicharacterslonginlengthsomereallylongusernamethatismorethan128asciicharacterslonginlength', 'password': 'muerle'})
        self.assertResponse(respData, count = None, errCode = testLib.RestTestCase.ERR_BAD_USERNAME)


# Unit test that tests the resetFixture function in UsersModel
class TestResetFixture(testLib.RestTestCase):
    def testReset1():
        self.makeRequest("/TESTAPI/resetfixture")
        self.makeRequest("/users/add", method="POST", data = {'user': 'james', 'password': 'muerle'})
        self.assertEqual(len(UsersModel.objects.all()), 1)
        self.makeRequest("/TESTAPI/resetfixture")
        self.assertEqual(len(UsersModel.objects.all()), 0)



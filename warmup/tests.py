import unittest
import testLib
from testAdditional import TestResponse


# Unit test that tests the login function in UsersModel
class TestUsersModel(TestResponse):
    # Make sure login succeeds after adding.
    def testLoginJames(self):
        self.makeRequest("/TESTAPI/resetFixture", method="POST")
        self.makeRequest("/users/add", method="POST", data = {'user': 'james', 'password': 'muerle'})
        respData = self.makeRequest("/users/login", method="POST", data = {'user': 'james', 'password': 'muerle'})
        self.assertResponse(respData, count = 2)


    # Make sure logging in multiple times increments the count.
    def testLoginSequence(self):
        self.makeRequest("/TESTAPI/resetFixture", method="POST")
        self.makeRequest("/users/add", method="POST", data = {'user': 'james', 'password': 'muerle'})
        respData = self.makeRequest("/users/login", method="POST", data = {'user': 'james', 'password': 'muerle'})
        # second login
        respData = self.makeRequest("/users/login", method="POST", data = {'user': 'james', 'password': 'muerle'})
        self.assertResponse(respData, count = 3)
        # third login
        respData = self.makeRequest("/users/login", method="POST", data = {'user': 'james', 'password': 'muerle'})
        self.assertResponse(respData, count = 4)
        # fourth login
        respData = self.makeRequest("/users/login", method="POST", data = {'user': 'james', 'password': 'muerle'})
        self.assertResponse(respData, count = 5)


    # Make sure adding a second user doesn't screw with the rest of the rows.
    def testLoginJames2(self):
        self.makeRequest("/TESTAPI/resetFixture", method="POST")
        self.makeRequest("/users/add", method="POST", data = {'user': 'james', 'password': 'muerle'})
        respData = self.makeRequest("/users/login", method="POST", data = {'user': 'james', 'password': 'muerle'})
        respData = self.makeRequest("/users/login", method="POST", data = {'user': 'james', 'password': 'muerle'})
        respData = self.makeRequest("/users/login", method="POST", data = {'user': 'james', 'password': 'muerle'})
        respData = self.makeRequest("/users/login", method="POST", data = {'user': 'james', 'password': 'muerle'})

        # Add second user
        self.makeRequest("/users/add", method="POST", data = {'user': 'james2', 'password': 'muerle'})
        respData = self.makeRequest("/users/login", method="POST", data = {'user': 'james2', 'password': 'muerle'})
        # Checks new user's count to be 1 (2 after logging in again)
        self.assertResponse(respData, count = 2)
        # Checks old user's count to still be 5 (6 after logging in again)
        respData = self.makeRequest("/users/login", method="POST", data = {'user': 'james', 'password': 'muerle'})
        self.assertResponse(respData, count = 6)


    # Make sure logging with incorrect username errors.
    def testLoginIncorrectUsername(self):
        self.makeRequest("/TESTAPI/resetFixture", method="POST")
        self.makeRequest("/users/add", method="POST", data = {'user': 'james', 'password': 'muerle'})
        respData = self.makeRequest("/users/login", method="POST", data = {'user': 'notjames', 'password': 'muerle'})
        self.assertResponse(respData, count = None, errCode = testLib.RestTestCase.ERR_BAD_CREDENTIALS)


    # Make sure logging with incorrect password errors.
    def testLoginIncorrectPassword(self):
        self.makeRequest("/TESTAPI/resetFixture", method="POST")
        self.makeRequest("/users/add", method="POST", data = {'user': 'james', 'password': 'muerle'})
        respData = self.makeRequest("/users/login", method="POST", data = {'user': 'james', 'password': 'notmuerle'})
        self.assertResponse(respData, count = None, errCode = testLib.RestTestCase.ERR_BAD_CREDENTIALS)


    # Make sure users are added to the database.
    def testAddTwoPeople(self):
        self.makeRequest("/TESTAPI/resetFixture", method="POST")
        self.makeRequest("/users/add", method="POST", data = {'user': 'james1', 'password': 'muerle'})
        self.makeRequest("/users/add", method="POST", data = {'user': 'james2', 'password': 'muerle'})
        respData = self.makeRequest("/users/login", method="POST", data = {'user': 'james1', 'password': 'muerle'})
        self.assertResponse(respData, count = 2)
        respData = self.makeRequest("/users/login", method="POST", data = {'user': 'james2', 'password': 'muerle'})
        self.assertResponse(respData, count = 2)


    # Make sure adding a user that exists gives an error.
    def testAddExistingUser(self):
        self.makeRequest("/TESTAPI/resetFixture", method="POST")
        self.makeRequest("/users/add", method="POST", data = {'user': 'james', 'password': 'muerle'})

        respData = self.makeRequest("/users/add", method="POST", data = {'user': 'james', 'password': 'some_password'})
        self.assertResponse(respData, count = None, errCode = testLib.RestTestCase.ERR_USER_EXISTS)


    # Make sure passwords can't be too long.
    def testAddLongPassword(self):
        self.makeRequest("/TESTAPI/resetFixture", method="POST")
        respData = self.makeRequest("/users/add", method="POST", data = {'user': 'notjames', 'password': 'somereallylongpasswordthatismorethan128asciicharacterslonginlengthsomereallylongpasswordthatismorethan128asciicharacterslonginlength'})
        self.assertResponse(respData, count = None, errCode = testLib.RestTestCase.ERR_BAD_PASSWORD)


    # Make sure usernames can't be too long nor empty.
    def testAddLongUsername(self):
        self.makeRequest("/TESTAPI/resetFixture", method="POST")
        respData = self.makeRequest("/users/add", method="POST", data = {'user': 'somereallylongusernamethatismorethan128asciicharacterslonginlengthsomereallylongusernamethatismorethan128asciicharacterslonginlength', 'password': 'muerle'})
        self.assertResponse(respData, count = None, errCode = testLib.RestTestCase.ERR_BAD_USERNAME)


    # Unit test that tests the resetFixture function in UsersModel
    def testResetFixture(self):
        respData = self.makeRequest("/TESTAPI/resetFixture", method="POST")
        respData = self.makeRequest("/users/add", method="POST", data = {'user': 'james', 'password': 'muerle'})
        self.assertResponse(respData)
        self.makeRequest("/TESTAPI/resetFixture", method="POST")
        respData = self.makeRequest("/users/login", method="POST", data = {'user': 'james', 'password': 'muerle'})
        self.assertResponse(respData, count = None, errCode = testLib.RestTestCase.ERR_BAD_CREDENTIALS)


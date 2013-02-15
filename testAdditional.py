import unittest
import testLib

# Class with assertResponse so I don't have to write it a bunch.
class TestResponse(testLib.RestTestCase):
    def assertResponse(self, respData, count = 1, errCode = testLib.RestTestCase.SUCCESS):
        """
        Check that the response data dictionary matches the expected values
        """
        expected = { 'errCode' : errCode }
        if count is not None:
            expected['count']  = count
        self.assertDictEqual(expected, respData)


# Class that tests normal usage of add, login, and resetFixture
class TestUsage(TestResponse):
    def testSimpleUsage(self):
        self.makeRequest("/TESTAPI/resetFixture", method="POST")

        # add james and check success
        respData = self.makeRequest("/users/add", method="POST", data = {'user': 'james', 'password': 'muerle'})
        self.assertResponse(respData)

        # login as james and check count
        respData = self.makeRequest("/users/login", method="POST", data = {'user': 'james', 'password': 'muerle'})
        self.assertResponse(respData, count = 2)

        # login as james2 and check success and database size
        respData = self.makeRequest("/users/add", method="POST", data = {'user': 'james2', 'password': 'muerle'})
        self.assertResponse(respData)

        # make sure that count was initialized to one for james2 in the database
        respData = self.makeRequest("/users/login", method="POST", data = {'user': 'james2', 'password': 'muerle'})
        self.assertResponse(respData, count = 2)

    def testDDOS(self):
        self.makeRequest("/TESTAPI/resetFixture", method="POST")

        # make a bunch of users and check database size
        numUsers = 10
        for i in range(0, numUsers):
            respData = self.makeRequest("/users/add", method="POST", data = {'user': 'james' + str(i), 'password': 'muerle' + str(i)})
            self.assertResponse(respData)

        # login a bunch of times as random users and check the login numbers for accuracy
        import random
        login_times = [random.randrange(10) for i in range(0, numUsers)]
        for i in range(0, numUsers):
            for times in range(0, login_times[i] + 1):
                self.makeRequest("/users/login", method="POST", data = {'user': 'james' + str(i), 'password': 'muerle' + str(i)})
        for i in range(0, numUsers):
                respData = self.makeRequest("/users/login", method="POST", data = {'user': 'james' + str(i), 'password': 'muerle' + str(i)})
                self.assertResponse(respData, count = login_times[i] + 3)


    def testLoginSequenceMixed(self):
        self.makeRequest("/TESTAPI/resetFixture", method="POST")

        # add and login james muerle
        respData = self.makeRequest("/users/add", method="POST", data = {'user': 'james', 'password': 'muerle'})
        self.assertResponse(respData)
        respData = self.makeRequest("/users/login", method="POST", data = {'user': 'james', 'password': 'muerle'})
        self.assertResponse(respData, count = 2)

        # add and login andrew finch
        respData = self.makeRequest("/users/add", method="POST", data = {'user': 'andrew', 'password': 'finch'})
        self.assertResponse(respData)
        respData = self.makeRequest("/users/login", method="POST", data = {'user': 'andrew', 'password': 'finch'})
        self.assertResponse(respData, count = 2)

        # add and login kevin fang
        respData = self.makeRequest("/users/add", method="POST", data = {'user': 'kevin', 'password': 'fang'})
        self.assertResponse(respData)
        respData = self.makeRequest("/users/login", method="POST", data = {'user': 'kevin', 'password': 'fang'})
        self.assertResponse(respData, count = 2)

        # Change the order a little bit
        respData = self.makeRequest("/users/login", method="POST", data = {'user': 'james', 'password': 'muerle'})
        self.assertResponse(respData, count = 3)
        respData = self.makeRequest("/users/login", method="POST", data = {'user': 'kevin', 'password': 'fang'})
        self.assertResponse(respData, count = 3)
        respData = self.makeRequest("/users/login", method="POST", data = {'user': 'andrew', 'password': 'finch'})
        self.assertResponse(respData, count = 3)

    def testResetFixture(self):
        self.makeRequest("/TESTAPI/resetFixture", method="POST")

        # create user
        respData = self.makeRequest("/users/add", method="POST", data = {'user': 'james', 'password': 'muerle'})
        self.assertResponse(respData)

        # clear database
        self.makeRequest("/TESTAPI/resetFixture", method="POST")

        # try to login and get bad credentials
        respData = self.makeRequest("/users/login", method="POST", data = {'user': 'james', 'password': 'muerle'})
        self.assertResponse(respData, count = None, errCode = RestTestCase.ERR_BAD_CREDENTIALS)


# Class for testing that making requests returns errors successfully.
class TestError(TestResponse):
    # Test errors that could happen when trying to log in.
    def testLoginError(self):
        self.makeRequest("/TESTAPI/resetFixture", method="POST")

        # login without adding is ERR_BAD_CREDENTIALS
        respData = self.makeRequest("/users/login", method="POST", data = {'user': 'james', 'password': 'muerle'})
        self.assertResponse(respData, count = None, errCode = RestTestCase.ERR_BAD_CREDENTIALS)

        # login after adding is successful
        self.makeRequest("/users/add", method="POST", data = {'user': 'james', 'password': 'muerle'})
        respData = self.makeRequest("/users/login", method="POST", data = {'user': 'james', 'password': 'muerle'})
        self.assertResponse(respData, count = 2)

    def testAddError(self):
        self.makeRequest("/TESTAPI/resetFixture", method="POST")

        # Check long password error
        respData = self.makeRequest("/users/add", method="POST", data = {'user': 'james', 'password': 'somereallylongpasswordthatinfringesourrequirementthatpasswordsbeonly128asciicharacterslongandidontknowhowtofilltherestofthispasswordup'})
        self.assertResponse(respData, count = None, errCode = RestTestCase.ERR_BAD_PASSWORD)

        # Make sure blank password is ok
        respData = self.makeRequest("/users/add", method="POST", data = {'user': 'james_blank_pw', 'password': ''})
        self.assertResponse(respData)

        # Adding same user is ERR_USER_EXISTS
        respData = self.makeRequest("/users/add", method="POST", data = {'user': 'james_blank_pw', 'password': 'muerle'})
        self.assertResponse(respData, count = None, errCode = RestTestCase.ERR_USER_EXISTS)

        # Check long username error
        respData = self.makeRequest("/users/add", method="POST", data = {'user': 'somereallylongusernamethatinfringesourrequirementthatusernamesbeonly128characterslongatmaximumineed30moreasciicharacterbutthisisalligot', 'password': 'muerle'})
        self.assertResponse(respData, count = None, errCode = RestTestCase.ERR_BAD_USERNAME)

        # Check empty username error
        respData = self.makeRequest("/users/add", method="POST", data = {'user': '', 'password': 'muerle'})
        self.assertResponse(respData, count = None, errCode = RestTestCase.ERR_BAD_USERNAME)







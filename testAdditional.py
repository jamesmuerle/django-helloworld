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


class TestUsage(TestResponse):
    def testSimpleUsage(self):
        # clear and check database size
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
        # clear and check database size
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


class TestError(TestResponse):
    def testLoginError(self):
        pass



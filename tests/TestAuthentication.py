import unittest
from services.registration import register
from services.authorization import authenticate
class TestAuthentication(unittest.TestCase):
    def testAuthenticateExistingUser(self):
        username = 'existingUser'
        password = 'pass'
        register(username, password)
        self.assertTrue(authenticate(username, password))

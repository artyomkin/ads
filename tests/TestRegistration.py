import unittest
import random
import string
from services.registration import register

class TestRegistration(unittest.TestCase):
    def testRegistrationNewUser(self):
        username = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        password = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        self.assertTrue(register(username, password))

    def testRegistrationExistingUser(self):
        username = 'existingUser'
        password = 'pass'
        register(username, password)
        self.assertFalse(register(username, password))

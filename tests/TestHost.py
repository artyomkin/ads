import unittest
import random
import string
from entities.Host import Host
from services.hostService import save, delete


class TestHost(unittest.TestCase):
    def testCreateNewHost(self):
        hostname = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        ip = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        sshUser = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        ownerUsername = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

        self.assertTrue(save(Host(hostname, ip, sshUser, ownerUsername)))

    def testDeleteExistingHost(self):
        hostname = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        ip = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        sshUser = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        ownerUsername = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

        save(Host(hostname, ip, sshUser, ownerUsername))

        self.assertTrue(delete(hostname))


    def testDeleteNonExistingHost(self):
        id = -1

        self.assertFalse(delete(id))

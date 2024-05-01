import unittest
import random
import string
from entities.Configuration import Configuration
from services.configService import save, delete
from DAO.ConfigurationDao import ConfigurationDao

class TestConfig(unittest.TestCase):
    def testCreateNewConfiguration(self):
        name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        path = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        ownerUsername = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

        self.assertTrue(save(Configuration(name, path, ownerUsername)))

    def testCreateExistingConfiguration(self):
        name = 'name'
        path = 'path'
        ownerUsername = 'someownerusername'
        save(Configuration(name, path, ownerUsername))

        self.assertFalse(save(Configuration(name, path, ownerUsername)))

    def testDeleteExistingConfiguration(self):
        name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        path = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        ownerUsername = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

        save(Configuration(name, path, ownerUsername))
        id = ConfigurationDao.objects.find(filter="name = '{}' and path = '{}'".format(name, path))[0]['id']
        self.assertTrue(delete(id))



    def testDeleteNonExistingConfiguration(self):
        id = -1

        self.assertFalse(delete(id))

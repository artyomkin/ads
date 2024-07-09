import queue
import unittest
import random
import string
from services.registration import register
from services.hostService import *
from services.hostGroupService import *
from services.authorization import *

class TestHosts(unittest.TestCase):
    def _gr(self):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    def testRegistrationNewUser(self):
        username = self._gr()
        password = self._gr()
        self.assertTrue(register(username, password))

    def testRegistrationExistingUser(self):
        username = 'existingUser'
        password = 'pass'
        register(username, password)
        self.assertFalse(register(username, password))

    def testHostCreate(self):
        hostname = self._gr()
        username = 'existingUser'
        ip = self._gr()
        ssh_user = self._gr()
        self.assertEqual(createHost(hostname, username, ip, ssh_user), (hostname, username))

    def testExistingHostCreate(self):
        hostname = 'existingHost'
        username = 'existingUser'
        ip = 'existingIp'
        ssh_user = 'existingSshUser'
        createHost(hostname, username, ip, ssh_user)
        self.assertIsNone(createHost(hostname, username, ip, ssh_user))

    def testHostGroupCreate(self):
        groupName = self._gr()
        self.assertIsNotNone(createHostGroup(groupName, 'existingUser'))

    def testHostAddToHostGroup(self):
        hostname = self._gr()
        username = 'existingUser'
        ssh_user = self._gr()
        ip = self._gr()
        createHost(hostname, username, ssh_user, ip)
        groupName = self._gr()
        createHostGroup(groupName, username)
        self.assertIsNotNone(addHostToGroup(hostname, groupName, username))

    def testHostGroupAddToHostGroup(self):
        groupName1 = self._gr()
        groupName2 = self._gr()
        createHostGroup(groupName1, 'existingUser')
        createHostGroup(groupName2, 'existingUser')
        self.assertIsNotNone(addHostGroupToHostGroup(groupName1, groupName2, 'existingUser'))

    def testGetParents(self):
        groupName1 = self._gr()
        groupName2 = self._gr()
        groupName3 = self._gr()
        groupId1 = createHostGroup(groupName1, 'existingUser')
        groupId2 = createHostGroup(groupName2, 'existingUser')
        groupId3 = createHostGroup(groupName3, 'existingUser')
        addHostGroupToHostGroup(groupName1, groupName2, 'existingUser')
        addHostGroupToHostGroup(groupName2, groupName3, 'existingUser')
        q = queue.Queue()
        q.put(groupId1)
        self.assertEqual(getAllRelatives(q, HostGroupDao.findParents), {groupId1, groupId2, groupId3})
        q = queue.Queue()
        q.put(groupId3)
        self.assertEqual(getAllRelatives(q, HostGroupDao.findChildren), {groupId1, groupId2, groupId3})



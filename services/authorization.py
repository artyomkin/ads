import queue

from DAO.UserDao import UserDao
from DAO.HostGroupDao import HostGroupDao
from DAO.HostDao import HostDao
from DAO.HostConfBindingDao import HostConfBindingDao
from DAO.ConfGroupDao import ConfGroupDao
import hashlib
import logging

logger = logging.getLogger(__name__)

def authorize(username, password):
    existingUser = UserDao.findByUsername(username)
    if existingUser is None:
        logger.info("User {} does not exist.".format(username))
        return False

    if hashlib.sha512(password.encode('utf-8')).hexdigest() == existingUser.password:
        logger.info("User {} successfully authenticated.".format(username))
        return True

    logger.info("User {} is not authenticated.".format(username))
    return False

def authorizeOnHost(hostname, username):
    return HostDao.exists(hostname, username)

def getAllRelatives(queue, findRelativesFunction, relatives=None):
    if queue.qsize() == 0:
        return relatives
    groupId = queue.get()
    if relatives == None:
        relatives = set()
    if groupId in relatives:
        return getAllRelatives(queue, findRelativesFunction, relatives)

    relatives.add(groupId)
    currelatives = findRelativesFunction(groupId)
    if currelatives is None or len(currelatives) == 0:
        if queue.qsize() == 0:
            return relatives
        else:
            return getAllRelatives(queue, findRelativesFunction, relatives)

    for curparent in currelatives:
        if curparent not in queue.queue:
            queue.put(curparent)
    return getAllRelatives(queue, findRelativesFunction, relatives=relatives)

def authorizeHostGroupOnConfGroup(hostGroupName, confGroupName, ownerUsername):
    hostGroupId = HostGroupDao.find(hostGroupName, ownerUsername)
    confGroupId = ConfGroupDao.find(confGroupName, ownerUsername)
    if hostGroupId is None or confGroupId is None:
        return False
    hostGroupId = hostGroupId[0]
    confGroupId = confGroupId[0]

    hostQueue = queue.Queue()
    hostQueue.put(hostGroupId)
    hostParents = getAllRelatives(hostQueue, HostGroupDao.findParents)

    confQueue = queue.Queue()
    confQueue.put(confGroupId)
    confParents = getAllRelatives(confQueue, ConfGroupDao.findParents)

    return any([ HostConfBindingDao.isBound(hgId, *confParents) for hgId in hostParents ])
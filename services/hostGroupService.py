import logging
import queue
from entities.declaration import Host, HostGroup
from DAO.HostDao import HostDao
from DAO.HostGroupDao import HostGroupDao

logger = logging.getLogger(__name__)


def createHostGroup(name, owner_username, childrenHosts=None, childrenHostGroups=None):
    if HostGroupDao.existsByNameAndUsername(name, owner_username):
        logger.info('Host group {} of {} already exists.'.format(name, owner_username))
        return None
    if childrenHostGroups is not None:
        for hostGroupName in childrenHostGroups:
            if not HostGroupDao.exists(hostGroupName, owner_username):
                return 1
    if childrenHosts is not None:
        for hostName in childrenHosts:
            if not HostDao.exists(hostName, owner_username):
                return 1

    if childrenHosts is not None:
        _childrenHosts = []
        for hostName in childrenHosts:
            _childrenHosts.append(HostDao.find(hostName, owner_username))
        hostGroup = HostGroup(name, owner_username, hosts=_childrenHosts)
        return HostGroupDao.save(hostGroup)
    elif childrenHostGroups is not None:
        _childrenHostGroups = []
        for hostGroupName in childrenHostGroups:
            _childrenHostGroups.append(HostGroupDao.find(hostGroupName, owner_username))
        hostGroup = HostGroup(name, owner_username, childrenHostGroups=_childrenHostGroups)
        return HostGroupDao.save(hostGroup)
    elif childrenHosts is None and childrenHostGroups is None:
        hostGroup = HostGroup(name, owner_username)
        return HostGroupDao.save(hostGroup)
    else:
        logger.info('Only one of hosts or childrentHostGroups should be specified for host group {} of {}.'.format(name,
                                                                                                                   owner_username))
        return None


def deleteHostGroup(name, owner_username):
    if not HostGroupDao.exists(name, owner_username):
        logger.info('Host group {} of {} does not exist.'.format(name, owner_username))
        return None
    result = HostGroupDao.delete(name, owner_username)
    return result


def addHostGroupToHostGroup(childHostGroupName, parentHostGroupName, ownerUsername):
    if not HostGroupDao.existsByNameAndUsername(childHostGroupName, ownerUsername) or not HostGroupDao.existsByNameAndUsername(parentHostGroupName,
                                                                                             ownerUsername):
        logger.info(
            'Host groups {} and {} of {} must exist.'.format(childHostGroupName, parentHostGroupName, ownerUsername))
        return None

    result = HostGroupDao.addHostGroupToHostGroup(childHostGroupName, parentHostGroupName, ownerUsername)
    if result is not None or len(result) > 0:
        return result

    logger.info('Could not add host group {} to host group {} of {}.'.format(childHostGroupName, parentHostGroupName,
                                                                             ownerUsername))
    return None


def deleteHostGroupFromHostGroup(childHostGroupName, parentHostGroupName, ownerUsername):
    if not HostGroupDao.exists(childHostGroupName, ownerUsername) or not HostGroupDao.exists(parentHostGroupName,
                                                                                             ownerUsername):
        logger.info(
            'Host groups {} and {} of {} must exist.'.format(childHostGroupName, parentHostGroupName, ownerUsername))
        return None

    result = HostGroupDao.deleteHostGroupFromHostGroup(childHostGroupName, parentHostGroupName, ownerUsername)
    if result is not None or len(result) > 0:
        return result

    logger.info(
        'Could not delete host group {} from host group {} of {}.'.format(childHostGroupName, parentHostGroupName,
                                                                          ownerUsername))
    return None

def convertGroupsToHosts(hostNames, ownerUsername):
    res = set()
    hostGroupsIds = [ HostGroupDao._getIdByNameAndOwnerUsername(hostName, ownerUsername) for hostName in hostNames ]
    for hostGroupId in hostGroupsIds:
        res.update(HostGroupDao.findHosts(hostGroupId))
    return list(res)

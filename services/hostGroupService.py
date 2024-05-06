import logging
from entities.declaration import Host, HostGroup
from DAO.HostDao import HostDao
from DAO.HostGroupDao import HostGroupDao

logger = logging.getLogger(__name__)

def createHostGroup(name, owner_username, hosts=None, childrenHostGroups=None):
    if hosts is not None:
        hostGroup = HostGroup(name, owner_username, hosts)
    elif childrenHostGroups is not None:
        hostGroup = HostGroup(name, owner_username, childrenHostGroups)
    else:
        logger.info('Only one of hosts or childrentHostGroups should be specified for host group {} of {}.'.format(name, owner_username))
        return None

    return HostGroupDao.save(hostGroup)


def deleteHostGroup(name, owner_username):
    if not HostGroupDao.exists(name, owner_username):
        logger.info('Host group {} of {} does not exist.'.format(name, owner_username))
        return None
    result = HostGroupDao.delete(name, owner_username)
    return result

def addHostGroupToHostGroup(childHostGroupName, parentHostGroupName, ownerUsername):
    if not HostGroupDao.exists(childHostGroupName, ownerUsername) or not HostGroupDao.exists(parentHostGroupName, ownerUsername):
        logger.info('Host groups {} and {} of {} must exist.'.format(childHostGroupName, parentHostGroupName, ownerUsername))
        return None

    result = HostGroupDao.addHostGroupToHostGroup(childHostGroupName, parentHostGroupName, ownerUsername)
    if result is not None or len(result) > 0:
        return result

    logger.info('Could not add host group {} to host group {} of {}.'.format(childHostGroupName, parentHostGroupName, ownerUsername))
    return None

def deleteHostGroupFromHostGroup(childHostGroupName, parentHostGroupName, ownerUsername):
    if not HostGroupDao.exists(childHostGroupName, ownerUsername) or not HostGroupDao.exists(parentHostGroupName, ownerUsername):
        logger.info('Host groups {} and {} of {} must exist.'.format(childHostGroupName, parentHostGroupName, ownerUsername))
        return None

    result = HostGroupDao.deleteHostGroupFromHostGroup(childHostGroupName, parentHostGroupName, ownerUsername)
    if result is not None or len(result) > 0:
        return result

    logger.info('Could not delete host group {} from host group {} of {}.'.format(childHostGroupName, parentHostGroupName, ownerUsername))
    return None

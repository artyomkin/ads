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

def addHostGroupToHostGroup(hostname, hostGroupName, owner_username):
    if not HostDao.exists(hostname, owner_username) or not HostGroupDao.exists(hostGroupName, owner_username):
        logger.info('Host {} and group {} of {} must exist'.format(hostname, hostGroupName, owner_username))
        return None
    result = HostGroupDao.addHostToGroup(hostname, owner_username, hostGroupName)
    return result

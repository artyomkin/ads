import logging
from entities.declaration import Host, HostGroup
from DAO.HostDao import HostDao
from DAO.HostGroupDao import HostGroupDao

logger = logging.getLogger(__name__)

def createHost(hostname, owner_username, ip, ssh_user):
    if HostDao.exists(hostname, owner_username):
        logger.info("Host {} of {} already exists".format(hostname, owner_username))
        return None

    host = Host(hostname, owner_username, ip, ssh_user)
    if len(HostDao.save(host)) > 0:
        logger.info("Successfully saved host {} of {}.".format(hostname, owner_username))
        return hostname, owner_username

    return None

def deleteHost(hostname, owner_username):
    if not HostDao.exists(hostname, owner_username):
        logger.info("Host {} of {} does not exist.".format(hostname, owner_username))
        return None

    result = HostDao.delete(hostname, owner_username)
    if len(result) > 0:
        logger.info("Successfully deleted {} of {}.".format(hostname, owner_username))
        return result

    return None

def addHostToGroup(hostname, host_group_name, owner_username):
    if not HostDao.exists(hostname, owner_username):
        logger.info("Host {} of {} does not exist.".format(hostname, owner_username))
        return None

    if HostGroupDao.exists(host_group_name, owner_username):
        result = HostGroupDao.addHostToGroup(hostname, owner_username, host_group_name)
        if result is not None and len(result) > 0:
            logger.info("Host {} of {} successfully added to host group {}.".format(hostname, owner_username, host_group_name))
            return result
    else:
        logger.info("Host group {} of {} does not exist.".format(hostname, host_group_name))

    return None

def deleteHostFromGroup(hostname, host_group_name, owner_username):
    if not HostDao.exists(hostname, owner_username):
        logger.info("Host {} of {} does not exist.".format(hostname, owner_username))
        return None

    if not HostGroupDao.exists(host_group_name, owner_username):
        logger.info("Hostgroup {} of {} does not exist.".format(host_group_name, owner_username))
        return None

    deleteRes = HostGroupDao.deleteHostFromGroup(hostname, host_group_name, owner_username)
    if deleteRes is not None and len(deleteRes) > 0:
        return deleteRes

    logger.info("Could not delete host {} from host group {} of {}.".format(hostname, host_group_name, owner_username))
    return None


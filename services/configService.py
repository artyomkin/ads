import logging
from entities.declaration import Configuration, ConfGroup
from DAO.ConfigurationDao import ConfigurationDao
from DAO.ConfGroupDao import ConfGroupDao

logger = logging.getLogger(__name__)

def createConf(name, owner_username, path):
    if ConfigurationDao.exists(name, owner_username):
        logger.info("Configuration {} of {} already exists.".format(name, owner_username))
        return None

    conf = Configuration(name, owner_username)
    if len(ConfigurationDao.save(conf)) > 0:
        logger.info("Successfully saved configuration {} of {}.".format(name, owner_username))
        return name, owner_username

    return None

def deleteConfig(name, owner_username):
    if not ConfigurationDao.exists(name, owner_username):
        logger.info("Configuration {} of {} does not exist.".format(name, owner_username))
        return None

    result = ConfigurationDao.delete(name, owner_username)
    if len(result) > 0:
        logger.info("Successfully deleted {} of {}.".format(name, owner_username))
        return result

    return None

def addConfToGroup(confName, confGroupName, ownerUsername):
    if not ConfigurationDao.exists(confName, ownerUsername):
        logger.info("Configuration {} of {} does not exist.".format(confName, ownerUsername))
        return None

    if ConfGroupDao.exists(confGroupName, ownerUsername):
        result = ConfGroupDao.addConfToGroup(confName, confGroupName, ownerUsername)
        if result is not None and len(result) > 0:
            logger.info("Configuration {} of {} successfully added to conf group {}.".format(confName, ownerUsername, confGroupName))
            return result
    else:
        logger.info("Configuration group {} of {} does not exist.".format(confGroupName, ownerUsername))

    return None

def deleteConfFromGroup(confName, confGroupName, ownerUsername):
    if not ConfigurationDao.exists(confName, ownerUsername):
        logger.info("Configuration {} of {} does not exist.".format(confName, ownerUsername))
        return None

    if not ConfGroupDao.exists(confGroupName, ownerUsername):
        logger.info("Configuration group {} of {} does not exist.".format(confGroupName, ownerUsername))
        return None

    deleteRes = ConfGroupDao.deleteConfFromGroup(confName, confGroupName, ownerUsername)
    if deleteRes is not None and len(deleteRes) > 0:
        return deleteRes

    logger.info("Could not delete configuration {} from configuration group {} of {}.".format(confName, confGroupName, ownerUsername))
    return None

def addConfGroupToConfGroup(childConfGroupName, parentConfGroupName, ownerUsername):
    if not ConfGroupDao.exists(childConfGroupName, ownerUsername) or not ConfGroupDao.exists(parentConfGroupName, ownerUsername):
        logger.info('Configuration groups {} and {} of {} must exist.'.format(childConfGroupName, parentConfGroupName, ownerUsername))
        return None

    result = ConfGroupDao.addConfGroupToConfGroup(childConfGroupName, parentConfGroupName, ownerUsername)
    if result is not None or len(result) > 0:
        return result

    logger.info('Could not add configuration group {} to configuration group {} of {}.'.format(childConfGroupName, parentConfGroupName, ownerUsername))
    return None

def deleteConfGroupFromConfGroup(childConfGroupName, parentConfGroupName, ownerUsername):
    if not ConfGroupDao.exists(childConfGroupName) or not ConfGroupDao.exists(parentConfGroupName):
        logger.info('Conf groups {} and {} of {} must exist.'.format(childConfGroupName, parentConfGroupName, ownerUsername))
        return None

    result = ConfGroupDao.deleteConfGroupFromConfGroup(childConfGroupName, parentConfGroupName, ownerUsername)
    if result is not None or len(result) > 0:
        return result

    logger.info('Could not delete configuration group {} from configuration group {} of {}.'.format(childConfGroupName, parentConfGroupName, ownerUsername))
    return None

def findConfsByOwner(username):
    return ConfigurationDao.findByOwner(username)

def createConfGroup(name, owner_username, childrenConfs=None, childrenConfGroups=None):
    if ConfGroupDao.exists(name, owner_username):
        logger.info('Configuration group {} of {} already exists.'.format(name, owner_username))
        return None
    if childrenConfGroups is not None:
        for confGroupName in childrenConfGroups:
            if not ConfGroupDao.exists(confGroupName, owner_username):
                return 1
    if childrenConfs is not None:
        for confName in childrenConfs:
            if not ConfigurationDao.exists(confName, owner_username):
                return 1

    if childrenConfs is not None:
        _childrenConfs = []
        for confName in childrenConfs:
            _childrenConfs.append(ConfigurationDao.find(confName, owner_username))
        confGroup = ConfGroup(name, owner_username, configurations=_childrenConfs)
        return ConfGroupDao.save(confGroup)
    elif childrenConfGroups is not None:
        _childrenConfGroups = []
        for confGroupName in childrenConfGroups:
            _childrenConfGroups.append(ConfGroupDao.find(confGroupName, owner_username))
        confGroup = ConfGroup(name, owner_username, childrenConfGroups=_childrenConfGroups)
        return ConfGroupDao.save(confGroup)
    elif childrenConfs is None and childrenConfGroups is None:
        confGroup = ConfGroup(name, owner_username)
        return ConfGroupDao.save(confGroup)
    else:
        logger.info('Only one of confs or children ConfGroups should be specified for conf group {} of {}.'.format(name, owner_username))
        return None

def deleteConfGroup(name, owner_username):
    if not ConfGroupDao.exists(name, owner_username):
        logger.info('Conf group {} of {} does not exist.'.format(name, owner_username))
        return None
    result = ConfGroupDao.delete(name, owner_username)
    return result

def convertGroupsToConf(confNames, ownerUsername):
    res = set()
    confGroupsIds = [ ConfGroupDao._getIdByNameAndOwnerUsername(confName, ownerUsername) for confName in confNames ]
    for confGroupId in confGroupsIds:
        res.update(ConfGroupDao.findConfs(confGroupId))
    return list(res)

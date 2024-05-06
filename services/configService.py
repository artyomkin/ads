import logging
from entities.declaration import Configuration, ConfGroup
from DAO.ConfigurationDao import ConfigurationDao
from DAO.ConfGroupDao import ConfGroupDao

logger = logging.getLogger(__name__)

#TODO - добавление конфига из указанного файла
def createConfig(name, owner_username):
    pass

#TODO - удаление файла конфига
def deleteConfig(name, owner_username):
    pass

def addConfToGroup(confName, confGroupName, ownerUsername):
    if not ConfigurationDao.exists(confName, ownerUsername):
        logger.info("Configuration {} of {} does not exist.".format(confName, ownerUsername))
        return None

    if ConfGroupDao.exists(confGroupName, ownerUsername):
        result = ConfGroupDao.addConfToGroup(confName, confGroupName, ownerUsername)
        if result is not None and len(result) > 0:
            logger.info("Configuration {} of {} successfully added to host group {}.".format(confName, ownerUsername, confGroupName))
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

#TODO - перенести в другой файл
def addConfGroupToConfGroup(childConfGroupName, parentConfGroupName, ownerUsername):
    if not ConfGroupDao.exists(childConfGroupName, ownerUsername) or not ConfGroupDao.exists(parentConfGroupName, ownerUsername):
        logger.info('Configuration groups {} and {} of {} must exist.'.format(childConfGroupName, parentConfGroupName, ownerUsername))
        return None

    result = ConfGroupDao.addConfGroupToConfGroup(childConfGroupName, parentConfGroupName, ownerUsername)
    if result is not None or len(result) > 0:
        return result

    logger.info('Could not add configuration group {} to configuration group {} of {}.'.format(childConfGroupName, parentConfGroupName, ownerUsername))
    return None

def deleteHostGroupFromHostGroup(childConfGroupName, parentConfGroupName, ownerUsername):
    if not ConfGroupDao.exists(childConfGroupName) or not ConfGroupDao.exists(parentConfGroupName):
        logger.info('Conf groups {} and {} of {} must exist.'.format(childConfGroupName, parentConfGroupName, ownerUsername))
        return None

    result = ConfGroupDao.deleteConfGroupFromConfGroup(childConfGroupName, parentConfGroupName, ownerUsername)
    if result is not None or len(result) > 0:
        return result

    logger.info('Could not delete configuration group {} from configuration group {} of {}.'.format(childConfGroupName, parentConfGroupName, ownerUsername))
    return None


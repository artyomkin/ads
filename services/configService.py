from DAO.ConfigurationDao import ConfigurationDao
import logging

logger = logging.getLogger(__name__)


def save(configuration):
    if ConfigurationDao.exists():
        existing_configuration = ConfigurationDao.objects.find(filter="path = '{}'".format(configuration.path))
        if existing_configuration is not None and len(existing_configuration) > 0:
            logger.info("Configuration {} with path {} already exists.".format(configuration.name, configuration.path))
            return False

    configurationDao = ConfigurationDao({
        "name": configuration.name,
        "path": configuration.path,
        "owner_username": configuration.owner_username
    })
    configurationDao.save()
    logger.info("Configuration {} with path {} successfully saved.".format(configuration.name, configuration.path))
    return True


def delete(id):
    existing_configuration = ConfigurationDao.objects.find(filter="id = {}".format(id))
    if existing_configuration is None or len(existing_configuration) == 0:
        logger.info("Configuration with id {} does not exist.".format(id))
        return False
    ConfigurationDao({"id": id}).delete()
    logger.info("Configuration with id {} was successfully deleted.".format(id))
    return True
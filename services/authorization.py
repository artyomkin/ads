from DAO.UserDao import UserDao
from DAO.HostDao import HostDao
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

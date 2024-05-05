from DAO.UserDao import UserDao
import hashlib
import logging

logger = logging.getLogger(__name__)


def authenticate(username, password):
    existingUser = UserDao.findByUsername(username)
    if existingUser is None:
        logger.info("User {} does not exist.".format(username))
        return False

    if hashlib.sha512(password.encode('utf-8')).hexdigest() == existingUser.password:
        logger.info("User {} successfully authenticated.".format(username))
        return True

    logger.info("User {} is not authenticated.".format(username))
    return False

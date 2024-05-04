from DAO import UserDao
import hashlib
import logging

logger = logging.getLogger(__name__)


def authenticate(username, password):
    existing_user = UserDao.objects.find(filter="username = '{}'".format(username))
    if existing_user is None or len(existing_user) == 0:
        logger.info("User {} does not exist.".format(username))
        return False

    # retrieve existing user from list
    existing_user = existing_user[0]

    if hashlib.sha512(password.encode('utf-8')).hexdigest() == existing_user['password']:
        logger.info("User {} successfully authenticated.".format(username))
        return True

    logger.info("User {} is not authenticated.".format(username))
    return False
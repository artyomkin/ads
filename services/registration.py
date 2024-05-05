import sqlite3

from DAO.UserDao import UserDao
import hashlib
import logging
from entities.declaration import User

logger = logging.getLogger(__name__)


def register(username, password):
    existingUser = UserDao.findByUsername(username)
    if existingUser is not None:
        logger.info("User {} already exists.".format(username))
        return False

    if UserDao.save(User(username, _encrypt(password))) == username:
        logger.info("User {} successfully registered.".format(username))
        return True
    else:
        logger.error("Could not register user {} because of unexpected error.".format(username))
        return False

def _encrypt(password):
    return hashlib.sha512(password.encode('utf-8')).hexdigest()
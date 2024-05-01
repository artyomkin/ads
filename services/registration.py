import sqlite3

from DAO.UserDao import UserDao
import hashlib
import logging

logger = logging.getLogger(__name__)


def register(username, password):
    if UserDao.exists():
        existing_user = UserDao.objects.find("username = '{}'".format(username))
        if existing_user is not None and len(existing_user) > 0:
            logger.info("User {} already exists.".format(username))
            return False

    userDao = UserDao({
        "username": username,
        "password": hashlib.sha512(password.encode('utf-8')).hexdigest()
    })
    if userDao.save() == 1:
        logger.info("User {} successfully registered.".format(username))
        return True
    else:
        logger.error("Could not register user {} because of unexpected error.".format(username))
        return False

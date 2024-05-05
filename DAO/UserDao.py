import sys

__import__('pysqlite3')
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from DAO.tableDeclaration import users, conn
from entities.declaration import User
from sqlalchemy import literal_column


class UserDao:
    @staticmethod
    def save(user):
        statement = users.insert().values(
            username=user.username,
            password=user.password
        ).returning(users.c.username)
        username = conn.execute(statement).fetchone()[0]
        conn.commit()
        return username

    @staticmethod
    def findByUsername(username):
        statement = users.select().where(users.c.username == username)
        existingUser = conn.execute(statement).fetchone()
        if existingUser is not None and len(existingUser) > 0:
            return User(*existingUser)
        else:
            return None

    @staticmethod
    def exists(username):
        statement = users.select().where(users.c.username == username)
        existingUser = conn.execute(statement)
        return existingUser is not None and len(existingUser) > 0


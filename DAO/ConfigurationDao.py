import sys

__import__('pysqlite3')
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from DAO.tableDeclaration import configurations, conn
from sqlalchemy import text

class ConfigurationDao:

    @staticmethod
    def save(*configList):
        configsValues = [ "('{}', '{}')".format(
            configItem.name,
            configItem.owner_username,
        ) for configItem in configList ]
        statement = text(
            "INSERT OR IGNORE INTO configurations VALUES {} returning name, owner_username". \
                format(", ".join(configsValues))
        )
        res = conn.execute(statement).fetchall()
        conn.commit()
        return res

    @staticmethod
    def exists(confName, ownerUsername):
        statement = configurations.select().where(
            configurations.c.name == confName,
            configurations.c.owner_username == ownerUsername
        )
        res = conn.execute(statement).fetchone()
        conn.commit()
        return res

    @staticmethod
    def delete(confName, ownerUsername):
        statement = configurations.delete().where(
            configurations.c.name == confName,
            configurations.c.owner_username == ownerUsername
        ).returning(
            configurations.c.name,
            configurations.c.owner_username
        )
        res = conn.execute(statement).fetchone()
        conn.commit()
        return res

    @staticmethod
    def findByOwner(username):
        statement = configurations.select().where(
            configurations.c.owner_username == username
        )
        result = conn.execute(statement).fetchall()
        return result

    @staticmethod
    def find(name, username):
        statement = configurations.select().where(
            configurations.c.owner_username == username,
            configurations.c.name == name
        )
        result = conn.execute(statement).fetchone()
        return result


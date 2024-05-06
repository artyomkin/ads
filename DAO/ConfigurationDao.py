import sys

__import__('pysqlite3')
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from tableDeclaration import configurations, conn
from sqlalchemy import text
from entities.declaration import Configuration

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

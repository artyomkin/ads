import sys

__import__('pysqlite3')
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from tableDeclaration import hosts, conn
from sqlalchemy import select, text
from entities.declaration import Host, User
from DAO.UserDao import UserDao
class HostDao:
    @staticmethod
    def save(*hostList):
        hostsValues = [ "('{}', '{}', '{}', '{}')".format(
            hostItem.hostname,
            hostItem.owner_username,
            hostItem.ip,
            hostItem.ssh_user
        ) for hostItem in hostList ]
        statement = text(
            "INSERT OR IGNORE INTO hosts VALUES {} RETURNING hostname, owner_username".\
            format(", ".join(hostsValues))
        )
        res = conn.execute(statement).fetchall()
        conn.commit()
        return res

    @staticmethod
    def exists(hostname, owner_username):
        statement = select(hosts.c.hostname).where(
            hosts.c.hostname == hostname,
            hosts.c.owner_username == owner_username
        )
        existingHostname = conn.execute(statement).fetchone()
        return existingHostname is not None

    @staticmethod
    def delete(hostname, owner_username):
        statement = hosts.delete().where(
            hosts.c.hostname == hostname,
            hosts.c.owner_username == owner_username
        ).returning(hosts.c.hostname, hosts.c.owner_username)
        deleteResult = conn.execute(statement).fetchone()
        conn.commit()
        return deleteResult


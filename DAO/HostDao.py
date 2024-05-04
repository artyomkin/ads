import sys

__import__('pysqlite3')
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from tableDeclaration import hosts, conn
from sqlalchemy import select, text
from entities.declaration import Host
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
            "INSERT OR IGNORE INTO hosts VALUES {} returning hostname, owner_username".\
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
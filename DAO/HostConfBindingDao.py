import sys

__import__('pysqlite3')
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from DAO.tableDeclaration import hostGroupToConfGroups, conn
from sqlalchemy import text

class HostConfBindingDao:
    @staticmethod
    def bind(hostGroupId, confGroupId):
        statement = hostGroupToConfGroups.insert().values(
            host_group_id = hostGroupId,
            conf_group_id = confGroupId
        ).returning(
            hostGroupToConfGroups.c.host_group_id,
            hostGroupToConfGroups.c.conf_group_id
        )
        res = conn.execute(statement).fetchone()
        conn.commit()
        return res

    @staticmethod
    def exists(hostGroupId, confGroupId):
        statement = hostGroupToConfGroups.select().where(
            hostGroupToConfGroups.c.host_group_id == hostGroupId,
            hostGroupToConfGroups.c.conf_group_id == confGroupId
        )
        res = conn.execute(statement).fetchone()
        return res is not None and len(res) > 0

    @staticmethod
    def isBound(hostGroupId, *confGroupIds):
        conditions = [
            "host_group_id = {} and conf_group_id = {}".\
                format(hostGroupId, confGroupId)
            for confGroupId in confGroupIds
        ]
        statement = text(
            "SELECT COUNT(*) FROM hostGroupToConfGroup WHERE {}". \
                format(" OR ".join(conditions))
        )
        res = conn.execute(statement).fetchone()[0]
        return res > 0

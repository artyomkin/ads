import sys

__import__('pysqlite3')
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from tableDeclaration import hostGroupToConfGroups, conn

class HostConfBindingDao:
    @staticmethod
    def bind(hostGroupId, confGroupId):
        statement = hostGroupToConfGroups.insert().values(
            host_group_id = hostGroupId,
            conf_group_id = confGroupId
        )
        conn.execute(statement)
        conn.commit()

import sys

__import__('pysqlite3')
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from HostDao import HostDao, UserDao
from DAO.tableDeclaration import hostGroups, hostToHostGroups, hostGroupToHostGroups, conn
from sqlalchemy import insert, select
from entities.declaration import Host, HostGroup, User

class HostGroupDao:
    @staticmethod
    def save(hostGroup):
        # if host group contains either hosts or host groups, raise exception
        if hostGroup.hosts is not None and hostGroup.childrenHostGroups is not None:
            raise Exception('Host group {} contains either hosts or host groups'.format(hostGroup.name))

        # save host group
        saveGroupStatement = hostGroups.insert().values(
            name = hostGroup.name,
            owner_username = hostGroup.owner_username
        ).returning(hostGroups.c.id)
        hostGroupId = conn.execute(saveGroupStatement).fetchone()[0]

        # save hosts
        if hostGroup.hosts is not None:
            conn.execute(
                insert(hostToHostGroups),
                [
                    {
                        "hostname": hostItem.hostname,
                        "host_owner_username": hostItem.owner_username,
                        "host_group_id": hostGroupId
                    }
                for hostItem in hostGroup.hosts]
            )

        # save host groups
        if hostGroup.childrenHostGroups is not None:
            conn.execute(
                insert(hostGroupToHostGroups),
                [
                    {
                        "host_group_child_id": hostGroupItem.id,
                        "host_group_parent_id": hostGroupId
                    }
                    for hostGroupItem in hostGroup.childrenHostGroups]
            )

        conn.commit()

        return hostGroupId

    @staticmethod
    def addHostToGroup(hostname, owner_username, host_group_name):
        findStatement = select(hostGroups.c.id).\
            select_from(hostGroups).\
            where(hostGroups.c.name == host_group_name)
        hostGroupId = conn.execute(findStatement).fetchone()[0]

        statement = hostToHostGroups.insert().values(
            hostname = hostname,
            host_owner_username = owner_username,
            host_group_id = hostGroupId
        ).returning(
            hostToHostGroups.c.hostname,
            hostToHostGroups.c.host_owner_username,
            hostToHostGroups.c.host_group_id
        )
        result = conn.execute(statement).fetchone()
        conn.commit()
        return result

    @staticmethod
    def deleteHostFromGroup(hostname, hostGroupName, owner_username):
        findStatement = select(hostGroups.c.id). \
            select_from(hostGroups). \
            where(hostGroups.c.name == hostGroupName)
        hostGroupId = conn.execute(findStatement).fetchone()[0]
        statement = hostToHostGroups.delete().\
        where(
            hostToHostGroups.c.hostname == hostname,
            hostToHostGroups.c.host_owner_username == owner_username,
            hostToHostGroups.c.hostGroupId == hostGroupId
        ).\
        returning(
            hostToHostGroups.c.hostname,
            hostToHostGroups.c.host_owner_username,
            hostToHostGroups.c.host_group_id
        )
        res = conn.execute(statement)
        conn.commit()
        return res

    @staticmethod
    def exists(id):
        statement = hostGroups.select().where(hostGroups.c.id == id)
        res = conn.execute(statement).fetchone()
        return res is not None and len(res) > 0

    @staticmethod
    def exists(name, owner_username):
        statement = hostGroups.select().where(hostGroups.c.name == name, hostGroups.c.owner_username == owner_username)
        res = conn.execute(statement).fetchone()
        return res is not None and len(res) > 0

    @staticmethod
    def delete(name, owner_username):
        statement = hostGroups.\
            delete().\
            where(hostGroups.c.name == name, hostGroups.c.owner_username == owner_username).\
            returning(hostGroups.c.name, hostGroups.c.owner_username)
        result = conn.execute(statement).fetchone()
        conn.commit()
        return result




#hostlist = [
#    Host('1hg1', 'o', 'i','s'),
#    Host('2hg1', 'o', 'i', 's'),
#    Host('1hg2', 'o', 'i', 's'),
#]

#UserDao.save(User('o', 'p'))
#HostDao.save(*hostlist)
#
#hostgroup1 = HostGroup('hg1', 'o')
#HostGroupDao.save(hostgroup1)
#
#HostGroupDao.addHostToGroup('1hg1', 'o', 'hg1')
#hostgroup2 = HostGroup('hg2', 'o', hosts=[hostlist[2]])
#hg1Id = HostGroupDao.save(hostgroup1)
#hg2Id = HostGroupDao.save(hostgroup2)
#hostgroup1.id = hg1Id
#hostgroup2.id = hg2Id
#hostgroup3 = HostGroup('hg3', 'o', childrenHostGroups=[hostgroup1, hostgroup2])
#HostGroupDao.save(hostgroup3)

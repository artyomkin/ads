import sys

__import__('pysqlite3')
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from DAO.tableDeclaration import hostGroups, hostToHostGroups, hostGroupToHostGroups, conn
from sqlalchemy import insert, select


class HostGroupDao:

    @staticmethod
    def _getIdByNameAndOwnerUsername(hostGroupName, ownerUsername):
        findStatement = select(hostGroups.c.id). \
            select_from(hostGroups). \
            where(hostGroups.c.name == hostGroupName, hostGroups.c.owner_username == ownerUsername)
        hostGroupId = conn.execute(findStatement).fetchone()[0]
        return hostGroupId

    @staticmethod
    def save(hostGroup):
        # if host group contains either hosts or host groups, raise exception
        if hostGroup.hosts is not None and hostGroup.childrenHostGroups is not None:
            raise Exception('Host group {} contains either hosts or host groups'.format(hostGroup.name))

        # save host group
        saveGroupStatement = hostGroups.insert().values(
            name=hostGroup.name,
            owner_username=hostGroup.owner_username
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
        hostGroupId = HostGroupDao._getIdByNameAndOwnerUsername(host_group_name, owner_username)

        statement = hostToHostGroups.insert().values(
            hostname=hostname,
            host_owner_username=owner_username,
            host_group_id=hostGroupId
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
        hostGroupId = HostGroupDao._getIdByNameAndOwnerUsername(hostGroupName, owner_username)
        statement = hostToHostGroups.delete(). \
            where(
            hostToHostGroups.c.hostname == hostname,
            hostToHostGroups.c.host_owner_username == owner_username,
            hostToHostGroups.c.hostGroupId == hostGroupId
        ). \
            returning(
            hostToHostGroups.c.hostname,
            hostToHostGroups.c.host_owner_username,
            hostToHostGroups.c.host_group_id
        )
        res = conn.execute(statement)
        conn.commit()
        return res

    @staticmethod
    def addHostGroupToHostGroup(childHostGroupName, parentHostGroupName, ownerUsername):
        childHostGroupId = HostGroupDao._getIdByNameAndOwnerUsername(childHostGroupName, ownerUsername)
        parentHostGroupId = HostGroupDao._getIdByNameAndOwnerUsername(parentHostGroupName, ownerUsername)

        statement = hostGroupToHostGroups.insert().values(
            host_group_child_id=childHostGroupId,
            host_group_parent_id=parentHostGroupId
        ).returning(
            hostGroupToHostGroups.c.host_group_child_id,
            hostGroupToHostGroups.c.host_group_parent_id
        )
        result = conn.execute(statement).fetchone()[0]
        conn.commit()
        return result

    @staticmethod
    def deleteHostGroupFromHostGroup(childHostGroupName, parentHostGroupName, ownerUsername):
        childHostGroupId = HostGroupDao._getIdByNameAndOwnerUsername(childHostGroupName, ownerUsername)
        parentHostGroupId = HostGroupDao._getIdByNameAndOwnerUsername(parentHostGroupName, ownerUsername)

        statement = hostGroupToHostGroups.delete().where(
            hostGroupToHostGroups.c.host_group_child_id == childHostGroupId,
            hostGroupToHostGroups.c.host_group_parent_id == parentHostGroupId
        ).returning(
            hostGroupToHostGroups.c.host_group_child_id,
            hostGroupToHostGroups.c.host_group_parent_id
        )
        result = conn.execute(statement).fetchone()[0]
        conn.commit()
        return result

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
        statement = hostGroups. \
            delete(). \
            where(hostGroups.c.name == name, hostGroups.c.owner_username == owner_username). \
            returning(hostGroups.c.name, hostGroups.c.owner_username)
        result = conn.execute(statement).fetchone()
        conn.commit()
        return result


#hostlist = [
#    Host('1hg1', 'oo', 'i','s'),
#    Host('2hg1', 'oo', 'i', 's'),
#    Host('1hg2', 'oo', 'i', 's'),
#]
#
#UserDao.save(User('oo', 'p'))
#HostDao.save(*hostlist)
#
#hostgroup1 = HostGroup('hg61', 'oo', hosts=[hostlist[0]])
#HostGroupDao.save(hostgroup1)
#hostgroup2 = HostGroup('hg62', 'oo', hosts=[hostlist[1]])
#HostGroupDao.save(hostgroup2)
#
#hostgroup3 = HostGroup('hg63', 'oo')
#HostGroupDao.save(hostgroup3)
#HostGroupDao.addHostToGroup('1hg2', 'oo', 'hg63')
#
#hg64 = HostGroup('hg64', 'oo')
#hg64id = HostGroupDao.save(hg64)
#hg64.id = hg64id
#HostGroupDao.addHostGroupToHostGroup('hg61', 'hg64', 'oo')
#HostGroupDao.addHostGroupToHostGroup('hg62', 'hg64', 'oo')
#
#hg65 = HostGroup('hg65', 'oo')
#hg65id = HostGroupDao.save(hg65)
#hg65.id = hg65id
#HostGroupDao.addHostGroupToHostGroup('hg63', 'hg65', 'oo')
#
#HostGroupDao.save(HostGroup('hg66', 'oo', childrenHostGroups=[hg64, hg65]))
#
#HostGroupDao.addHostToGroup('1hg1', 'o', 'hg1')
#hostgroup2 = HostGroup('hg2', 'o', hosts=[hostlist[2]])
#hostgroup1.id = hg1Id
#hostgroup2.id = hg2Id
#hostgroup3 = HostGroup('hg3', 'o', childrenHostGroups=[hostgroup1, hostgroup2])
#HostGroupDao.save(hostgroup3)


#conflist = [
#    Configuration('1hg1', 'oo'),
#    Configuration('2hg1', 'oo'),
#    Configuration('1hg2', 'oo'),
#]
#
#UserDao.save(User('oo', 'p'))
#ConfigurationDao.save(*conflist)
#
#confgroup1 = ConfGroup('hg61', 'oo', configurations=[conflist[0]])
#ConfGroupDao.save(confgroup1)
#confgroup2 = ConfGroup('hg62', 'oo', configurations=[conflist[1]])
#ConfGroupDao.save(confgroup2)
#
#confgroup3 = ConfGroup('hg63', 'oo')
#ConfGroupDao.save(confgroup3)
#ConfGroupDao.addConfToGroup('1hg2', 'hg63', 'oo')
#
#hg64 = ConfGroup('hg64', 'oo')
#hg64id = ConfGroupDao.save(hg64)
#hg64.id = hg64id
#ConfGroupDao.addConfGroupToConfGroup('hg61', 'hg64', 'oo')
#ConfGroupDao.addConfGroupToConfGroup('hg62', 'hg64', 'oo')
#
#hg65 = ConfGroup('hg65', 'oo')
#hg65id = ConfGroupDao.save(hg65)
#hg65.id = hg65id
#ConfGroupDao.addConfGroupToConfGroup('hg63', 'hg65', 'oo')
#
#ConfGroupDao.save(ConfGroup('hg66', 'oo', childrenConfGroups=[hg64, hg65]))

#ConfigurationDao.delete('1hg1', 'oo')
#ConfGroupDao.delete('hg63', 'oo')
#UserDao.delete('oo')

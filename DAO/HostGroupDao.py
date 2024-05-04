import sys

__import__('pysqlite3')
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from HostDao import HostDao
from DAO.tableDeclaration import hostGroups, hostToHostGroups, hostGroupToHostGroups, conn
from sqlalchemy import insert
from entities.declaration import Host, HostGroup

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

#hostlist = [
#    Host('1hg1', 'o', 'i','s'),
#    Host('2hg1', 'o', 'i', 's'),
#    Host('1hg2', 'o', 'i', 's'),
#]
#
#HostDao.save(*hostlist)
#
#hostgroup1 = HostGroup('hg1', 'o', hosts=[hostlist[0],hostlist[1]])
#hostgroup2 = HostGroup('hg2', 'o', hosts=[hostlist[2]])
#hg1Id = HostGroupDao.save(hostgroup1)
#hg2Id = HostGroupDao.save(hostgroup2)
#hostgroup1.id = hg1Id
#hostgroup2.id = hg2Id
#hostgroup3 = HostGroup('hg3', 'o', childrenHostGroups=[hostgroup1, hostgroup2])
#HostGroupDao.save(hostgroup3)

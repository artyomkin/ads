import sys

__import__('pysqlite3')
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from ConfigurationDao import ConfigurationDao
from DAO.tableDeclaration import confGroups, confToConfGroups, confGroupToConfGroups, conn
from sqlalchemy import insert
from entities.declaration import Configuration, ConfGroup

class ConfGroupDao:
    @staticmethod
    def save(confGroup):
        # if conf group contains either configurations or configuration groups, raise exception
        if confGroup.configurations is not None and confGroup.childrenConfGroups is not None:
            raise Exception('Conf group {} contains either configurations or configuration groups'.format(confGroup.name))

        # save conf group
        saveGroupStatement = confGroups.insert().values(
            name = confGroup.name,
            owner_username = confGroup.owner_username
        ).returning(confGroups.c.id)
        confGroupId = conn.execute(saveGroupStatement).fetchone()[0]

        # save configurations
        if confGroup.configurations is not None:
            conn.execute(
                insert(confToConfGroups),
                [
                    {
                        "conf_name": confItem.name,
                        "conf_owner_username": confItem.owner_username,
                        "conf_group_id": confGroupId
                    }
                for confItem in confGroup.configurations]
            )

        # save conf groups
        if confGroup.childrenConfGroups is not None:
            conn.execute(
                insert(confGroupToConfGroups),
                [
                    {
                        "conf_group_child_id": confGroupItem.id,
                        "conf_group_parent_id": confGroupId
                    }
                    for confGroupItem in confGroup.childrenConfGroups]
            )

        conn.commit()

        return confGroupId

#conflist = [
#    Configuration('1cg1', 'o'),
#    Configuration('2cg1', 'o'),
#    Configuration('1cg2', 'o')
#]
#
#ConfigurationDao.save(*conflist)
#
#confgroup1 = ConfGroup('cg1', 'o', configurations=[conflist[0],conflist[1]])
#confgroup2 = ConfGroup('cg2', 'o', configurations=[conflist[2]])
#cg1Id = ConfGroupDao.save(confgroup1)
#cg2Id = ConfGroupDao.save(confgroup2)
#confgroup1.id = cg1Id
#confgroup2.id = cg2Id
#confgroup3 = ConfGroup('cg3', 'o', childrenConfGroups=[confgroup1, confgroup2])
#print(ConfGroupDao.save(confgroup3))

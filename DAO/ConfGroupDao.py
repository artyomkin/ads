import sys

__import__('pysqlite3')
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from DAO.tableDeclaration import confGroups, confToConfGroups, confGroupToConfGroups, conn
from sqlalchemy import insert, select

class ConfGroupDao:
    @staticmethod
    def _getIdByNameAndOwnerUsername(name, ownerUsername):
        findStatement = select(confGroups.c.id). \
            select_from(confGroups). \
            where(confGroups.c.name == name, confGroups.c.owner_username == ownerUsername)
        res = conn.execute(findStatement).fetchone()
        if res is not None and len(res) > 0:
            return res[0]
        return None
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

    @staticmethod
    def exists(confGroupName, ownerUsername):
        statement = confGroups.select().where(
            confGroups.c.name == confGroupName,
            confGroups.c.owner_username == ownerUsername
        )
        result = conn.execute(statement).fetchone()
        return result

    @staticmethod
    def delete(name, ownerUsername):
        statement = confGroups.delete().where(
            confGroups.c.name == name,
            confGroups.c.owner_username == ownerUsername
        ).returning(
            confGroups.c.name,
            confGroups.c.owner_username
        )
        result = conn.execute(statement).fetchone()
        conn.commit()
        return result

    @staticmethod
    def addConfToGroup(confName, confGroupName, ownerUsername):
        confGroupId = ConfGroupDao._getIdByNameAndOwnerUsername(confGroupName, ownerUsername)
        statement = confToConfGroups.insert().values(
            conf_name = confName,
            conf_owner_username = ownerUsername,
            conf_group_id = confGroupId
        ).returning(
            confToConfGroups.c.conf_name,
            confToConfGroups.c.conf_owner_username,
            confToConfGroups.c.conf_group_id
        )
        res = conn.execute(statement).fetchone()
        conn.commit()
        return res

    @staticmethod
    def deleteConfFromGroup(confName, confGroupName, ownerUsername):
        confGroupId = ConfGroupDao._getIdByNameAndOwnerUsername(confGroupName, ownerUsername)
        statement = confToConfGroups.delete().where(
            confToConfGroups.c.conf_name == confName,
            confToConfGroups.c.conf_owner_username == ownerUsername,
            confToConfGroups.c.conf_group_id == confGroupId
        ).returning(
            confToConfGroups.c.conf_name,
            confToConfGroups.c.conf_owner_username,
            confToConfGroups.c.conf_group_id
        )
        res = conn.execute(statement).fetchone()
        conn.commit()
        return res

    @staticmethod
    def addConfGroupToConfGroup(childConfGroupName, parentConfGroupName, ownerUsername):
        childConfGroupId = ConfGroupDao._getIdByNameAndOwnerUsername(childConfGroupName, ownerUsername)
        parentConfGroupId = ConfGroupDao._getIdByNameAndOwnerUsername(parentConfGroupName, ownerUsername)
        statement = confGroupToConfGroups.insert().values(
            conf_group_child_id = childConfGroupId,
            conf_group_parent_id = parentConfGroupId
        ).returning(
            confGroupToConfGroups.c.conf_group_child_id,
            confGroupToConfGroups.c.conf_group_parent_id
        )
        res = conn.execute(statement).fetchone()
        conn.commit()
        return res

    @staticmethod
    def deleteConfGroupFromConfGroup(childConfGroupName, parentConfGroupName, ownerUsername):
        childConfGroupId = ConfGroupDao._getIdByNameAndOwnerUsername(childConfGroupName, ownerUsername)
        parentConfGroupId = ConfGroupDao._getIdByNameAndOwnerUsername(parentConfGroupName, ownerUsername)
        statement = confToConfGroups.delete().where(
            confGroupToConfGroups.c.conf_group_child_id == childConfGroupId,
            confGroupToConfGroups.c.conf_group_parent_id == parentConfGroupId
        ).returning(
            confGroupToConfGroups.c.conf_group_child_id,
            confGroupToConfGroups.c.conf_group_parent_id
        )
        res = conn.execute(statement).fetchone()
        conn.commit()
        return res

    @staticmethod
    def find(name, username):
        statement = confGroups.select().where(
            confGroups.c.owner_username == username,
            confGroups.c.name == name
        )
        result = conn.execute(statement).fetchone()
        return result


    @staticmethod
    def findByOwner(username):
        statement = confGroups.select().where(
            confGroups.c.owner_username == username
        )
        result = '\n'.join([ confGroup.name for confGroup in conn.execute(statement).fetchall() ])
        return result

    @staticmethod
    def findParents(childId):
        statement = confGroupToConfGroups.select().where(
            confGroupToConfGroups.c.conf_group_child_id == childId
        )
        res = conn.execute(statement).fetchall()
        if res is not None:
            return [ item[1] for item in res ]
        return None

    @staticmethod
    def findChildren(parentId):
        statement = confGroupToConfGroups.select().where(
            confGroupToConfGroups.c.conf_group_parent_id == parentId
        )
        res = conn.execute(statement).fetchall()
        if res is not None:
            return [item[0] for item in res]
        return None

    @staticmethod
    def findConfs(groupId):
        statement = confToConfGroups.select().where(
            confToConfGroups.c.conf_group_id == groupId
        )
        res = conn.execute(statement).fetchall()
        if res is not None:
            return [(item[0], item[1]) for item in res]
        return None


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

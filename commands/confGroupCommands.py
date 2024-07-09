from services.configService import *
from commands.argumentParser import parseArguments
from services.authorization import *
import services.configService

def show(kvargs, args):
    if not authorize(kvargs.get('username'), kvargs.get('password')):
        return 1, "Unauthorized."

    result = ConfGroupDao.findByOwner(kvargs.get('username'))
    return 0, result

def create(kvargs, args):
    if not authorize(kvargs.get('username'), kvargs.get('password')):
        return 1, "Unauthorized."

    groupName = args[0]
    username = kvargs.get('username')
    childrenGroups = None
    childrenConfs = None
    if 'children-confs' in kvargs and 'children-groups' in kvargs:
        return 1, "Configuration group must consist of confs or conf groups only"
    if 'children-confs' in kvargs:
        childrenConfs = kvargs.get('children-confs').split(',')
    if 'children-groups' in kvargs:
        childrenGroups = kvargs.get('children-groups').split(',')
    result = createConfGroup(groupName, username, childrenConfGroups=childrenGroups, childrenConfs=childrenConfs)
    if result == 1:
        return 1, "Cannot create {}. Invalid data.".format(groupName)
    elif result is not None:
        return 0, groupName
    return 1, "Conf group {} already exists.".format(groupName)

def delete(kvargs, args):
    if not authorize(kvargs.get('username'), kvargs.get('password')):
        return 1, "Unauthorized."
    groupName = args[0]
    username = kvargs.get('username')
    res = deleteConfGroup(groupName, username)
    if res is not None:
        return 0, res
    return 1, "Configuration group {} does not exist.".format(groupName)

def addConfToGroup(kvargs, args):
    if not authorize(kvargs.get('username'), kvargs.get('password')):
        return 1, "Unauthorized."
    confname = args[0]
    confGroupName = args[1]
    username = kvargs.get('username')
    res = services.configService.addConfToGroup(confname, confGroupName, username)
    if res is not None:
        return 0, res
    return 1, "Conf group {} does not exist.".format(confGroupName)

def addConfGroupToGroup(kvargs, args):
    if not authorize(kvargs.get('username'), kvargs.get('password')):
        return 1, "Unauthorized."
    childConfGroupName = args[0]
    parentConfGroupName = args[1]
    username = kvargs.get('username')
    res = addConfGroupToConfGroup(childConfGroupName, parentConfGroupName, username)
    if res is not None:
        return 0, res
    return 1, "Conf group {} or {} does not exist.".format(childConfGroupName, parentConfGroupName)

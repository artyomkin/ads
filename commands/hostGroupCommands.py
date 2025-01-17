from services.hostGroupService import *
from commands.argumentParser import parseArguments
from services.authorization import *
import services.hostService

def show(kvargs, args):
    if not authorize(kvargs.get('username'), kvargs.get('password')):
        return 1, "Unauthorized."

    result = HostGroupDao.findByOwner(kvargs.get('username'))
    return 0, result

def create(kvargs, args):
    if not authorize(kvargs.get('username'), kvargs.get('password')):
        return 1, "Unauthorized."

    groupName = args[0]
    username = kvargs.get('username')
    childrenGroups = None
    childrenHosts = None
    if 'children-hosts' in kvargs and 'children-groups' in kvargs:
        return 1, "Host group must consist of hosts or host groups only"
    if 'children-hosts' in kvargs:
        childrenHosts = kvargs.get('children-hosts').split(',')
    if 'children-groups' in kvargs:
        childrenGroups = kvargs.get('children-groups').split(',')
    result = createHostGroup(groupName, username, childrenHostGroups=childrenGroups, childrenHosts=childrenHosts)
    if result == 1:
        return 1, "Cannot create {}. Invalid data.".format(groupName)
    elif result is not None:
        return 0, groupName
    return 1, "Host group {} already exists.".format(groupName)

def delete(kvargs, args):
    if not authorize(kvargs.get('username'), kvargs.get('password')):
        return 1, "Unauthorized."
    groupName = args[0]
    username = kvargs.get('username')
    res = deleteHostGroup(groupName, username)
    if res is not None:
        return 0, res
    return 1, "Host group {} does not exist.".format(groupName)

def addHostToGroup(kvargs, args):
    if not authorize(kvargs.get('username'), kvargs.get('password')):
        return 1, "Unauthorized."
    hostname = args[0]
    hostGroupName = args[1]
    username = kvargs.get('username')
    res = services.hostService.addHostToGroup(hostname, hostGroupName, username)
    if res is not None:
        return 0, res
    return 1, "Host group {} does not exist.".format(hostGroupName)

def addHostGroupToGroup(kvargs, args):
    if not authorize(kvargs.get('username'), kvargs.get('password')):
        return 1, "Unauthorized."
    childHostGroupName = args[0]
    parentHostGroupName = args[1]
    username = kvargs.get('username')
    res = addHostGroupToHostGroup(childHostGroupName, parentHostGroupName, username)
    if res is not None:
        return 0, res
    return 1, "Host group {} or {} does not exist.".format(childHostGroupName, parentHostGroupName)

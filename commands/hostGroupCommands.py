from services.hostGroupService import *
from commands.argumentParser import parseArguments
from services.authorization import *

#TODO - не работает
def create(kvargs, args):
    if not authorize(kvargs.get('username'), kvargs.get('password')):
        return 1, "Unauthorized."

    groupName = args[0]
    username = kvargs.get('username')
    childrenGroups = None
    if len(args) > 1:
        childrenGroups = args[1:]
    result = createHostGroup(groupName, username, childrenHostGroups=childrenGroups)
    if result is not None:
        return 0, groupName

    return 1, "Host group {} already exists.".format(groupName)

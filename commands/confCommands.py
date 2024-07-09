from services.configService import *
from commands.argumentParser import parseArguments
from services.authorization import *

def show(kvargs, args):
    if not authorize(kvargs.get('username'), kvargs.get('password')):
        return 1, "Unauthorized."

    output = '\n'.join([ conf.name for conf in findConfsByOwner(kvargs.get('username')) ])
    return 0, output

def create(kvargs, args):
    if not authorize(kvargs.get('username'), kvargs.get('password')):
        return 1, "Unauthorized."

    confname = args[0]
    if createConf(confname, kvargs.get('username'), None) is not None:
        return 0, confname
    return 1, "Configuration {} already exists.".format(confname)

def delete(kvargs, args):
    confname = args[0]
    if not authorize(kvargs.get('username'), kvargs.get('password')):
        return 1, "Unauthorized."

    if deleteConfig(confname, kvargs.get('username')) is not None:
        return 0, confname

    return 1, "Unauthorized."


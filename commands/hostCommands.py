from services.hostService import *
from commands.argumentParser import parseArguments
from services.authorization import *

def show(kvargs, args):
    if not authorize(kvargs.get('username'), kvargs.get('password')):
        return 1, "Unauthorized."

    output = '\n'.join([ host.hostname for host in findHostsByOwner(kvargs.get('username')) ])
    return 0, output

def create(kvargs, args):
    if not authorize(kvargs.get('username'), kvargs.get('password')):
        return 1, "Unauthorized."

    hostname = args[0]
    ip = args[1]
    ssh_user = args[2]
    if createHost(hostname, kvargs.get('username'), ip, ssh_user) is not None:
        return 0, hostname
    return 1, "Host {} already exists.".format(hostname)

def delete(kvargs, args):
    hostname = args[0]
    if not authorize(kvargs.get('username'), kvargs.get('password')):
        return 1, "Unauthorized."

    if deleteHost(hostname, kvargs.get('username')) is not None:
        return 0, hostname

    return 1, "Unauthorized."


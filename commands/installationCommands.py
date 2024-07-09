from services.hostGroupService import *
from commands.argumentParser import parseArguments
from services.authorization import *
import services.hostGroupService
import services.configService
from deploy.deploy import runDeploy

def install(kvargs, args):
    if not authorize(kvargs.get('username'), kvargs.get('password')):
        return 1, "Unauthorized."

    hostGroupNames = args[0].split(',')
    confGroupNames = args[1].split(',')
    for hostGroupName in hostGroupNames:
        for confGroupName in confGroupNames:
            if not authorizeHostGroupOnConfGroup(hostGroupName, confGroupName, kvargs.get('username')):
                return 1, "{} is not authorized to install {}.".format(hostGroupName, confGroupName)

    hosts = services.hostGroupService.convertGroupsToHosts(hostGroupNames, kvargs.get('username'))
    confs = services.configService.convertGroupsToConf(confGroupNames, kvargs.get('username'))
    runDeploy(hosts, confs)
    return 0, "Ok."

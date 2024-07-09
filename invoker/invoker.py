import commands.hostCommands
import commands.hostGroupCommands
import commands.confGroupCommands
import commands.confCommands
import commands.installationCommands
import commands.registerCommands
from commands.argumentParser import parseArguments
commands = {
    'host-show': commands.hostCommands.show,
    'host-create': commands.hostCommands.create,
    'host-delete': commands.hostCommands.delete,
    'host-group-show': commands.hostGroupCommands.show,
    'host-group-create': commands.hostGroupCommands.create,
    'host-group-delete': commands.hostGroupCommands.delete,
    'host-group-add-host': commands.hostGroupCommands.addHostToGroup,
    'host-group-add-host-group': commands.hostGroupCommands.addHostGroupToGroup,
    'conf-show': commands.confCommands.show,
    'conf-create': commands.confCommands.create,
    'conf-delete': commands.confCommands.delete,
    'conf-group-show': commands.confGroupCommands.show,
    'conf-group-create': commands.confGroupCommands.create,
    'conf-group-delete': commands.confGroupCommands.delete,
    'conf-group-add-conf': commands.confGroupCommands.addConfToGroup,
    'conf-group-add-conf-group': commands.confGroupCommands.addConfGroupToGroup,
    'deploy': commands.installationCommands.install,
    'register': commands.registerCommands.register
}

def invoke(commandName, arguments):
    kvargs, args = parseArguments(arguments)
    if not commands.__contains__(commandName):
        return 1, "Command {} not found.".format(commandName)
    return commands.get(commandName)(kvargs, args)
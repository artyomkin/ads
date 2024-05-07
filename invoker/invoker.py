import commands.hostCommands
import commands.hostGroupCommands
from commands.argumentParser import parseArguments
commands = {
    'host-show': commands.hostCommands.show,
    'host-create': commands.hostCommands.create,
    'host-delete': commands.hostCommands.delete,
    'host-group-create': commands.hostGroupCommands.create
    #TODO - написать команды
}

def invoke(commandName, arguments):
    kvargs, args = parseArguments(arguments)
    if not commands.__contains__(commandName):
        return 1, "Command {} not found.".format(commandName)
    return commands.get(commandName)(kvargs, args)

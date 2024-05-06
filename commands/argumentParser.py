import re
def parseArguments(arguments):
    kvArgs = {}
    otherArgs = []
    flagPattern = re.compile("^--.*$")
    i = 0
    while i < len(arguments):
        if flagPattern.match(arguments[i]):
            if i+1 >= len(arguments):
                raise Exception('Flag without value.')
            kvArgs[arguments[i][2:]] = arguments[i+1]
            i += 1
        else:
            otherArgs.append(arguments[i])
        i+=1
    return kvArgs, otherArgs

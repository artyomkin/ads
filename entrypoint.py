import sys
from invoker.invoker import invoke
import logging

logger = logging.getLogger(__name__)

arguments = sum([ arg.split('=') for arg in sys.argv ], [])
#arguments = ['entrypoint.py', 'host-delete', '--username', 'o', '--password', 'p', 'hello']
if len(arguments) < 2:
    logging.error('At least 2 arguments myst be specified.')
    exit(1)

commandName = arguments[1]
arguments = arguments[2:]

exitCode, output = invoke(commandName, arguments)
print(output)
exit(exitCode)

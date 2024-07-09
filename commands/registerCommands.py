import services.registration
from services.registration import *
def register(kvargs, args):
    username = services.registration.register(args[0], args[1])
    if username is not None:
        return 0, username
    return 1, "User already exists."
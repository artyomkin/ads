class Configuration:
    def __init__(self, name, owner_username):
        self.name = name
        self.owner_username = owner_username

class ConfGroup:
    def __init__(self, name, owner_username, configurations=None, childrenConfGroups=None):
        self.name = name
        self.owner_username = owner_username
        self.configurations = configurations
        self.childrenConfGroups = childrenConfGroups


class Host:
    def __init__(self, hostname, owner_username, ip, ssh_user):
        self.hostname = hostname
        self.ip = ip
        self.ssh_user = ssh_user
        self.owner_username = owner_username


class HostGroup:
    def __init__(self, name, owner_username, hosts=None, childrenHostGroups=None, id=None):
        self.name = name
        self.owner_username = owner_username
        self.hosts = hosts
        self.childrenHostGroups = childrenHostGroups

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
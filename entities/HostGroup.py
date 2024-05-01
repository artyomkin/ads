class HostGroup:
    def __init__(self, name, owner_username, hosts=None, hostGroups=None, id=None):
        self.id = id
        self.name = name
        self.owner_username = owner_username
        self.hosts = hosts
        self.hostGroups = hostGroups

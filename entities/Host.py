class Host:
    def __init__(self, hostname, ip, ssh_user, owner_username, id=None):
        self.id = id
        self.hostname = hostname
        self.ip = ip
        self.ssh_user = ssh_user
        self.owner_username = owner_username
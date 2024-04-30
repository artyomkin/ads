class Host:
    def __init__(self, hostname, ip, ssh_user, ssh_password):
        self.hostname = hostname
        self.ip = ip
        self.ssh_user = ssh_user
        self.ssh_password = ssh_password
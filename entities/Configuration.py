class Configuration:
    def __init__(self, name, path, owner_username, id=None):
        self.id = id
        self.name = name
        self.path = path
        self.owner_username = owner_username
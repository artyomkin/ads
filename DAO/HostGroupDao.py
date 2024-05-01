import orm_sqlite


db = orm_sqlite.Database('example.db')
class HostToGroupDao(orm_sqlite.Model):
    hostId = orm_sqlite.IntegerField()
    hostGroupId = orm_sqlite.IntegerField()


class HostGroupDao(orm_sqlite.Model):
    id = orm_sqlite.IntegerField(primary_key=True)
    name = orm_sqlite.StringField()
    owner_username = orm_sqlite.StringField()

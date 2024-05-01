import orm_sqlite

db = orm_sqlite.Database('example.db')

class HostDao(orm_sqlite.Model):
    id = orm_sqlite.IntegerField(primary_key=True)
    hostname = orm_sqlite.StringField()
    ip = orm_sqlite.StringField()
    ssh_user = orm_sqlite.StringField()
    owner_username = orm_sqlite.StringField()

HostDao.objects.backend = db

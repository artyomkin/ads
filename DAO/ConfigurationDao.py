import orm_sqlite

db = orm_sqlite.Database('example.db')

class ConfigurationDao(orm_sqlite.Model):
    id = orm_sqlite.IntegerField(primary_key=True)
    name = orm_sqlite.StringField()
    path = orm_sqlite.StringField()
    owner_username = orm_sqlite.IntegerField()

ConfigurationDao.objects.backend = db

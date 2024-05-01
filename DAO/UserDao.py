import orm_sqlite
from entities.User import User

db = orm_sqlite.Database('example.db')


class UserDao(orm_sqlite.Model):
    id = orm_sqlite.IntegerField(primary_key=True)
    username = orm_sqlite.StringField()
    password = orm_sqlite.StringField()


UserDao.objects.backend = db

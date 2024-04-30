import sqlite3
import orm_sqlite
class MyUser(orm_sqlite.Model):
    id = orm_sqlite.IntegerField(primary_key=True)
    username = orm_sqlite.StringField()
    password = orm_sqlite.StringField()

db = orm_sqlite.Database('example.db')
MyUser.objects.backend = db

someUser = MyUser({'username': 'hello', 'password': 'world'})
someUser.save()

#print(User.objects.all())

import sys

__import__('pysqlite3')
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from tableDeclaration import users, conn
class UserDao:
    @staticmethod
    def save(user):
        statement = users.insert().values(
            username=user.username,
            password=user.password
        ).returning(users.c.username)
        username = conn.execute(statement).fetchone()[0]
        conn.commit()
        return username

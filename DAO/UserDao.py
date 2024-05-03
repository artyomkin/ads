__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
from sqlalchemy import create_engine
from tableDeclaration import users

class UserDao:
    def __init__(self):
        self.engine = create_engine("sqlite:///test.db")
        self.conn = self.engine.connect()
    '''
    Метод __del__() вызывается для любого объекта, когда счетчик ссылок для этого объекта становится равным нулю.
    Счетчик ссылок для данного объекта становится нулевым, когда работа программы завершается, или мы удаляем все ссылки вручную с помощью ключевого слова del.
    Деструктор не будет запускаться при удалении какой-то одной ссылки на объект. Он будет вызываться только тогда, когда все ссылки на объект будут удалены.
    '''
    def __del__(self):
        self.conn.close()

    def save(self, user):
        statement = users.insert().\
            values(
                username = user.username,
                password = user.password
            ).\
            returning(users.c.username)
        username = self.conn.execute(statement).fetchone()[0]
        return username

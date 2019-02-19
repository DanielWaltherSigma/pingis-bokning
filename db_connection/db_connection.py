from peewee import *
from db_connection.configuration import dbconf


class DbConnection(object):
    __instance = None

    def __new__(cls):
        if DbConnection.__instance is None:
            DbConnection.__instance = object.__new__(cls)
            DbConnection.__instance.val = object()
            DbConnection.__init_mysql()

        return DbConnection.__instance

    def get_connection(self):
        return self.__instance.val

    @staticmethod
    def __init_mysql():
        DbConnection.__instance.val = MySQLDatabase(dbconf['name'],
                                                host=dbconf['host'],
                                                port=dbconf['port'],
                                                user=dbconf['user'],
                                                passwd=dbconf['passwd'])
        print("Connection set up")


class BaseModel(Model):
    class Meta:
        database = DbConnection().get_connection()

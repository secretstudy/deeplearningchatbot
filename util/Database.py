import pymysql
import pymysql.cursors
import logging

class Database:
    '''

     '''

    def __init__(self,host,user,password,db_name, charset='utf-8'):
        self.host = host
        self.user = user
        self.password = password
        self.charset = charset
        self.db_name = db_name
        self.conn = None
"""
dict项目用于数据处理
"""

import pymysql
import hashlib
import time


# 编写一个功能类,提供给服务端使用
class Database:
    def __init__(self, host='localhost',
                 port=3306,
                 database='dict',
                 user='root',
                 passwd='123456',
                 charset='utf8'):
        self.host = host
        self.database = database
        self.port = port
        self.user = user
        self.passwd = passwd
        self.charset = charset
        self.connect_db()  # 连接数据库

    def connect_db(self):
        """
        创建db对象,连接数据库
        :return:
        """
        self.db = pymysql.connect(host=self.host,
                                  port=self.port,
                                  passwd=self.passwd,
                                  user=self.user,
                                  database=self.database,
                                  charset=self.charset)

    def create_cursor(self):
        """
        创建游标
        :return:
        """
        self.cur = self.db.cursor()

    def close(self):
        """
        关闭数据库
        :return:
        """
        self.cur.close()
        self.db.close()

    def register(self, name, passwd):
        """
        处理注册
        :param name:
        :param passwd:
        :return:
        """
        sql = "select * from user where name='%s';" % name
        self.cur.execute(sql)
        if self.cur.fetchone():  # 如果查询到结果
            return False
        # 加密处理
        hash = hashlib.md5((name + "哎呦我去").encode())
        hash.update(passwd.encode())
        sql = "insert into user (name,passwd) values (%s,%s);"

        try:
            self.cur.execute(sql, [name, hash.hexdigest()])
            self.db.commit()
            return True
        except Exception:
            self.db.rollback()
            return False

    def login(self, name, passwd):
        """
            处理客户的登录
        :param name:
        :param passwd:
        :return:
        """
        hash = hashlib.md5((name + "哎呦我去").encode())
        hash.update(passwd.encode())
        sql = "select * from user  where name='%s' and passwd='%s'" % (name, hash.hexdigest())
        self.cur.execute(sql)
        if self.cur.fetchone():
            return True
        return False

    def query(self, word):
        """
        查单词
        :param name:
        :param word:
        :return:
        """
        sql = "select mean from words where word='%s';" % word
        self.cur.execute(sql)
        r = self.cur.fetchone()
        if r:
            return r[0]
        else:
            return

    def insert_history(self, name, word):
        """
            插入历史记录
        :param name:
        :param word:
        :return:
        """
        tm = time.ctime()
        sql = "insert into  hist (name,word,time) values (%s,%s,%s);"
        try:
            self.cur.execute(sql, [name, word, tm])
            self.db.commit()
        except Exception:
            self.db.rollback()

    def find_history(self,name):
        """
        查询历史记录
        :param name:
        :param num:
        :return:
        """
        sql = "select name,word,time from hist where name='%s' order by id desc limit 10;" % name
        self.cur.execute(sql)
        return self.cur.fetchall()

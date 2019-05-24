"""
dict 服务端
处理请求逻辑
"""

from socket import *
from multiprocessing import Process
from time import sleep
import signal
import sys
from operation_db import *

# 全局变量
HOST = '0.0.0.0'
PORT = 8888
ADDR = (HOST, PORT)


# 处理注册
def do_register(c, db, data):
    tmp = data.split(" ")
    name = tmp[1]
    passwd = tmp[2]

    if db.register(name, passwd):
        c.send(b'OK')
    else:
        c.send(b'Fal')

# 处理登录
def do_login(c, db, data):
    tmp = data.split(" ")
    name = tmp[1]
    passwd = tmp[2]
    if db.login(name, passwd):
        c.send(b'OK')
    else:
        c.send(b'FAL')

#处理查询单词
def do_query(c, db, data):
    tmp = data.split(" ")
    name = tmp[1]
    word = tmp[2]

    # 插入历史记录
    db.insert_history(name, word)

    # 查询单词
    mean = db.query(word)

    if not mean:
        c.send("该单词不存在".encode())
    else:
        msg = "%s : %s" % (word, mean)
        c.send(msg.encode())

#处理历史记录查询
def do_history(c, db, data):
    tmp = data.split(" ")
    name = tmp[1]
    info = db.find_history(name)
    if not info:
        c.send(b'FAIL')
        return
    c.send(b'OK')
    for item in info:
        # item==>(name,word,time)
        msg = "%s         %-10s           %s" % item
        sleep(0.1)  # 防止粘包
        c.send(msg.encode())

    sleep(0.1)
    c.send(b'##')

# 处理客户端请求
def do_request(c, db):
    db.create_cursor()  # 生成游标 db.cur
    while True:
        data = c.recv(1024).decode()
        # print(c.getpeername(), ':', data)
        if not data or data[0] == 'E':
            # db.close() 若写在此处会导致登录一次就无法链接数据库
            c.close()
            # print("客户端退出")
            return
            # sys.exit("客户端退出")
        elif data[0] == 'R':
            do_register(c, db, data)
        elif data[0] == 'L':
            do_login(c, db, data)
        elif data[0] == 'Q':
            do_query(c, db, data)
        elif data[0] == "H":
            do_history(c, db, data)

# 网络连接
def main():
    # 创建数据库连接对象
    db = Database()

    # 创建tcp套接字
    s = socket()
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind(ADDR)
    s.listen(5)

    # 处理僵尸进程
    signal.signal(signal.SIGCHLD, signal.SIG_IGN)

    # 等待客户端的连接
    print("Listen the port 8888...")
    while True:
        try:
            c, addr = s.accept()
            print("Connect from", addr)
        except KeyboardInterrupt:
            s.close()
            db.close()
            sys.exit("服务器退出")
        except Exception as e:
            print(e)
            continue
        # 创建子进程
        p = Process(target=do_request, args=(c, db))
        p.daemon = True
        p.start()


if __name__ == '__main__':
    main()

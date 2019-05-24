"""
dict 服务端
发起请求,展示结果
"""

from socket import *
from getpass import getpass
import sys

ADDR = ('176.234.8.11', 8888)

# 所有函数都用s
s = socket()
s.connect(ADDR)


# 登录
def do_login():
    name = input("User:")
    passwd = getpass("Passwd:")
    msg = "L %s %s" % (name, passwd)
    s.send(msg.encode())
    # 等待反馈
    data = s.recv(128).decode()
    if data == "OK":
        print("登录成功")
        login(name)
    else:
        print("登录失败")


def do_query(name):
    while True:
        word = input("请输入要查询的单词:")
        if word == "##":  # 结束单词查询
            break
        msg = 'Q %s %s' % (name, word)
        s.send(msg.encode())
        data = s.recv(2048).decode()
        # 显示查询结果
        print(data)


def do_history(name):
    msg = 'H %s' % (name)
    s.send(msg.encode())
    data = s.recv(128).decode()
    if data == 'OK':
        while True:
            data = s.recv(1024).decode()
            if data == '##':
                break
            print(data)
    else:
        print("没有查询记录")


# 二级界面
def login(name):
    while True:
        print("""
        ================Query================
          1.查单词    2.历史记录     3. 注销
        =====================================
        """)
        cmd = input("输入选项:")
        if cmd == '1' or cmd == '查单词':
            do_query(name)
        elif cmd == '2' or cmd == '历史记录':
            do_history(name)
        elif cmd == '3' or cmd == '注销':
            return
        else:
            print("请输入正确命令!!!")


# 注册
def do_register():
    while True:
        name = input("User:")
        passwd = getpass("Passwd:")
        passwd1 = getpass("Again:")

        if (' ' in name) or (' ' in passwd) or (' ' in passwd1):
            print("用户名或密码不能有空格!!!")
            continue
        if passwd != passwd1:
            print("两次密码不一致")
            continue

        msg = 'R %s %s' % (name, passwd)
        # 发送请求
        s.send(msg.encode())
        # 接受反馈
        data = s.recv(128).decode()
        if data == "OK":
            print("注册成功")
            login(name)
        else:
            print("注册失败")
        return


# 创建网络连接
def main():
    try:
        while True:
            print("""
            ===============Welcome===============
             1. 注册        2.登录       3. 退出
            =====================================
            """)
            cmd = input("输入选项:")
            if cmd == '1' or cmd == '注册':
                do_register()
            elif cmd == '2' or cmd == '登录':
                do_login()
            elif cmd == '3' or cmd == '退出':
                s.send(b'E')
                print("谢谢使用")
                return
            else:
                print("请输入正确命令!!!")
    except KeyboardInterrupt:
        sys.exit("\n退出成功")


if __name__ == '__main__':
    main()

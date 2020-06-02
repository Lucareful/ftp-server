# -- coding=utf-8 --
"""
@author:luenci
@time:2020/6/2 17:40
"""
# import socket
#
# sk =socket.socket()
# sk.connect(("127.0.0.1",8001))
import json
import optparse
import socket


class ClientHandler(object):
    def __init__(self):
        self.op = optparse.OptionParser()
        self.op.add_option("-s", "--server", dest="server")
        self.op.add_option("-P", "--port", dest="port")
        self.op.add_option("-U", "--username", dest="username")
        self.op.add_option("-p", "--password", dest="password")

        self.options, self.args = self.op.parse_args()

        self.verify_args(self.options, self.args)

        self.make_connection()

    def verify_args(self, options, args):
        server = options.server
        port = options.port
        # 端口校验
        if 0 < int(port) < 65535:
            return True
        else:
            print("端口范围有误...")

    def make_connection(self):
        self.sock = socket.socket()
        self.sock.connect((self.options.server, int(self.options.port)))

    def interactive(self):
        self.authenticate()

    def authenticate(self):
        if self.options.username is None or self.options.password is None:
            username = input("username: ")
            password = input("password: ")
            return self.get_auth_result(username, password)
        else:
            return self.get_auth_result(self.options.username, self.options.password)

    def response(self):
        data = self.sock.recv(1024).decode("utf-8")
        data = json.loads(data)
        return data

    def get_auth_result(self, usr, pwd):
        data = {
            "action": "auth",
            "username": usr,
            "password": pwd
        }
        # print(json.dumps(data).encode("utf-8"))
        self.sock.send(json.dumps(data).encode("utf-8"))
        response = self.response()
        print(response)


ch = ClientHandler()
ch.interactive()

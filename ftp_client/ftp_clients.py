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
import os
import socket

STATUS_CODE = {
    250: "Invalid cmd format",
    251: "Invalid cmd",
    252: "Invalid auth data",
    253: "Wrong username or password",
    254: "Passed authentication",
    255: "Filename doesn't provided",
    256: "File doesn't exits on server",
    257: "ready to send file",
    258: "md5 verification",

    800: "the file exits, but not enough, is continue?",
    801: "the file exit !",
    802: "ready to receive datas",

    900: "md5 verify success !"
}


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

        self.mian_path = os.path.dirname(os.path.abspath(__file__))

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
        if self.authenticate():
            print("server is begin......")
            cmd_info = input("[%s]" % self.user).strip()
            cmd_list = cmd_info.split()
            if hasattr(self, cmd_list[0]):
                func = getattr(self, cmd_list[0])
                func(cmd_list)

    def put(self, *cmd_list):
        # put test.png images
        action,local_path,target_path = cmd_list
        local_path = os.path.join(self.mian_path, local_path)

        file_name = os.path.basename(local_path)
        file_size = os.stat(local_path).st_size

        data = {
            "action":"put",
            "file_name":file_name,
            "file_size":file_size,
            "target_path":target_path
        }

        self.sock.send(json.dumps(data).encode("utf-8"))

        is_exits = self.sock.recv(1024).decode("utf-8")
        has_send = 0
        if is_exits=="800":
            # 文件不完整
            pass
        elif is_exits=="801":
            # 文件完全存在
            return
        else:
            pass
        f = open(local_path,"rb")
        while has_send <file_size:
            data = f.read(1024)
            self.sock.sendall(data)
            has_send += len(data)

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

    def get_auth_result(self, user, pwd):
        data = {
            "action": "auth",
            "username": user,
            "password": pwd
        }
        # print(json.dumps(data).encode("utf-8"))
        self.sock.send(json.dumps(data).encode("utf-8"))
        response = self.response()
        # print(STATUS_CODE[response["status_code"]])
        if response["status_code"] == 254:
            self.user = user
            print(STATUS_CODE[254])
            return True
        else:
            print(STATUS_CODE[response["status_code"]])


ch = ClientHandler()
ch.interactive()

# -- coding=utf-8 --
"""
@author:luenci
@time:2020/6/2 19:03
"""
import json
import configparser
import os
import socketserver
from conf import settings

STATUS_CODE = {
    250: "Invalid cmd format",
    251: "Invalid cmd",
    252: "Invalid auth data",
    253: "Wrong username or password",
    254: "Passed authentication",
    255: "Filename doesn't provided",
    256: "File doesn't exist on server",
    257: "ready to send file",
    258: "md5 verification",

    800: "the file exist, but not enough, is continue?",
    801: "the file exist !",
    802: "ready to receive datas",

    900: "md5 verify success !"
}


class ServerHandler(socketserver.BaseRequestHandler):
    def handle(self):
        # print('ok')
        while True:
            data = self.request.recv(1024).strip()
            data = json.loads(data.decode("utf-8"))

            """
            {
                "action":"auth",
                "username":XXX,
                "pwd":XXX
            }
            """
            if data.get("action"):
                if hasattr(self, data.get("action")):
                    func = getattr(self, data.get("action"))
                    func(**data)
                else:
                    print("Not Found")
            else:
                print("Invalid cmd")

    def send_response(self, status_code):
        response = {"status_code": status_code}

        self.request.sendall(json.dumps(response).encode('utf-8'))

    def auth(self, **data):
        # {'action': 'auth', 'username': 'luenci', 'password': '123'}
        username = data['username']
        password = data['password']

        usr = self.authenticate(username, password)
        if usr:
            self.send_response(254)

        else:
            self.send_response(253)

    def authenticate(self, user, pwd):
        config = configparser.ConfigParser()
        config.read(settings.USER_INFO)

        if user in config.sections():
            if config[user]['password'] == pwd:
                self.user = user
                self.main_path = os.path.join(settings.BASE_DIR, "home")
                return user

    def put(self, **data):
        print("data:", data)
        file_name = data.get("file_name")
        file_size = data.get("file_size")
        target_path = data.get("target_path")

        abs_path = os.path.join(self.main_path, target_path, file_name)
        has_received = 0
        if os.path.exists(abs_path):
            file_has_size = os.stat(abs_path).st_size
            if file_has_size < file_size:
                # 断点续传
                self.request.sendall("800".encode("utf-8"))
                choice = self.request.recv(1024).decode("utf-8")
                if choice == "Y":
                    self.request.sendall(str(file_has_size).encode("utf-8"))
                    has_received += file_has_size
                    f = open(abs_path, "ab")
                else:
                    f = open(abs_path, "wb")
            else:
                # 文件完整存在
                self.request.sendall('801'.encode("utf-8"))
                return
        else:
            self.request.sendall("802".encode("utf-8"))
            f = open(abs_path, "wb")

        while has_received < file_size:
            try:
                data = self.request.recv(1024)
            except Exception as e:
                break
            f.write(data)
            has_received += len(data)

        f.close()

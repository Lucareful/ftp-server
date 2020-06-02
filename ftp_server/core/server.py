# -- coding=utf-8 --
"""
@author:luenci
@time:2020/6/2 19:03
"""
import json
import configparser
import socketserver


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

    def auth(self, **data):
        # {'action': 'auth', 'username': 'luenci', 'password': '123'}
        username = data['username']
        password = data['password']
        config = configparser.ConfigParser()
        config.read('UserDataBase.cfg')

    def put(self, **data):
        pass

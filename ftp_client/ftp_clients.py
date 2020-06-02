# -- coding=utf-8 --
"""
@author:luenci
@time:2020/6/2 17:40
"""
# import socket
#
# sk =socket.socket()
# sk.connect(("127.0.0.1",8001))
import optparse


class ClientHandler(object):
    def __init__(self):
        self.op = optparse.OptionParser()
        self.op.add_options("-s", "--server", dest="server")
        self.op.add_options("-P", "--port", dest="port")
        self.op.add_options("-U", "--username", dest="username")
        self.op.add_options("-p", "--password", dest="password")

        options,args = self.op.parse_args()

        self.verify_args(options,args)
    def verify_args(self,options,args):
        server = options.server
        port = options.port




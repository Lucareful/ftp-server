# -- coding=utf-8 --
"""
@author:luenci
@time:2020/6/2 17:43
"""
import optparse
import socketserver
from conf import settings
from core import server


class ArgvHandler(object):
    def __init__(self):
        self.op = optparse.OptionParser()
        options, args = self.op.parse_args()
        self.verify_args(options, args)

    def verify_args(self, options, args):
        cmd = args[0]
        if hasattr(self, cmd):
            func = getattr(self, cmd)
            func()

    def start(self):
        print("server is working")
        s = socketserver.ThreadingTCPServer((settings.IP, settings.PORT), server.ServerHandler)
        s.serve_forever()

    def help(self):
        pass

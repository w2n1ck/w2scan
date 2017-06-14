#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
@Author：W2n1ck
@Index：http://www.w2n1ck.com/
'''

import traceback


class PocInfoWrong(Exception):
    def __init__(self, info):
        Exception.__init__(self, "{}不完整,info有待补充项,必须要完善的author, name, imp_version, description, repair, "
                                 "type".format(info))


class PocOptionsWrong(Exception):
    def __init__(self, options):
        Exception.__init__(self, "{}不完整,option有待补充项,必须要完善的host, port".format(options))


class TargetsRepeat(Exception):
    def __init__(self):
        Exception.__init__(self, "targets,files两者只能设置一个")


class TargetsError(Exception):
    def __init__(self):
        Exception.__init__(self, "请至少设置一个targets或者files")


class PluginsError(Exception):
    def __init__(self):
        Exception.__init__(self, "请向plugins填写一个插件")


class PluginsNotFound(Exception):
    def __init__(self, args):
        Exception.__init__(self, "{}插件不存在".format(args))


class LevelError(Exception):
    def __init__(self):
        Exception.__init__(self,"level等级应该在1-4之间的整数")


def check_info(info):
    if not isinstance(info, dict):
        raise TypeError("传入的info不是一个dict类型")
    if not (info.has_key("author") and info.has_key("name") and info.has_key("imp_version") \
                    and info.has_key("description") and info.has_key("repair") and info.has_key("type")):
        raise PocInfoWrong(info)


def check_options(options):
    if not isinstance(options, dict):
        raise TypeError("传入的options不是一个dict类型")
    if not (options.has_key("host") and options.has_key("port")):
        raise PocOptionsWrong(options)

def check_config(info, options):
    result = True
    try:
        check_info(info)
        check_options(options)
    except (PocInfoWrong, PocOptionsWrong, TypeError), e:
        print traceback.print_exc()
        result = False
    return result
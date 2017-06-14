#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
@Author：W2n1ck
@Index：http://www.w2n1ck.com/
'''
import argparse
import sys
import json
sys.path.append("../..")
from flask.common.taskschedule import task_schedule
from flask.common.util import load_plugin
from flask.common.exception.poc_exception import TargetsError
from flask.common.exception.poc_exception import PluginsError
from flask.common.exception.poc_exception import PluginsNotFound
from flask.common.exception.poc_exception import LevelError
from flask.common.exception.poc_exception import TargetsRepeat
from flask.common.util.string_inject_dic import string_to_dic
from flask.plugins import plugin_config

def print_logo():
    print '----------------------------------------------'
    print '|   __        ______  ____                   |'
    print '|   \ \      / /___ \/ ___|  ___ __ _ _ __   |'
    print "|    \ \ /\ / /  __) \___ \ / __/ _` | '_ \  |"
    print '|     \ V  V /  / __/ ___) | (_| (_| | | | | |'
    print '|      \_/\_/  |_____|____/ \___\__,_|_| |_| |'
    print '|                                            |'
    print '----------------------------------------------'
    print '[+] Author : W2n1ck'
    print '[+] Index  : http://www.w2n1ck.com/'
    print '[+] Email  : admin@w2n1ck.com'
    print '++++++++++++++++++++++++++++++++++++++++++++++'

def help():
    parser = argparse.ArgumentParser()
    parser.add_argument("--targets", required=False, help="扫描目标 eg:www.baidu.com,www.google.com")
    parser.add_argument("--plugins", required=False, help="调用插件 eg:redis, structs")
    parser.add_argument("--files", required=False, help="扫描目标文件 eg:file.txt")
    parser.add_argument("--level", type=int, default=1, help = "等级 eg:1-4")
    parser.add_argument("--headers", default="{}", required=False, help="扫描配置,设置http请求头,应对登录情况 eg:"
                                                              "{\\\"Cookie\\\":\\\"JSESSIONID=***\\\"}")
    parser.add_argument("--list", action="store_true", help="列出所有可以利用的插件模块", default=False)
    parser.add_argument("--debug", default=False, help="debug模式,默认不展示,可以设置为true")
    args = parser.parse_args()
    return args


def list_modles(args):
    if args.list:
        plugin_config.get_modles()
        exit()


def get_parserdata(args):
    try:
        list_modles(args)
        debug = parser_debug(args)
        targets = parser_targets(args)
        plugins = parser_plugins(args)
        level = parser_level(args)
        headers = parser_headers(args)
    except (TargetsError, PluginsError, LevelError, TargetsRepeat), e:
        print str(e)
        exit()
    return targets, plugins, level, debug, headers


def parser_headers(args):
    try:
        result = string_to_dic(args.headers)
    except ValueError, e:
        print "{}不是一个有效的格式".format(args.headers)
    return result



def parser_debug(args):
    result = True if args.debug and args.debug == "true" else False
    return result


def parser_level(args):
    if not (args.level and isinstance(args.level, int) and args.level > 0 and args.level < 5):
        raise LevelError()
    return args.level


def parser_plugins(args):
    if not args.plugins:
        raise PluginsError
    return string_list(args.plugins)


def parser_targets(args):
    if not args.targets and not args.files:
        raise TargetsError()
    if args.targets and args.files:
        raise TargetsRepeat()
    if args.targets:
        return string_list(args.targets)
    elif args.files:
        return file_list(args.files)


def file_list(file_name):
    files = None
    result = []
    try:
        files = open(file_name)
        result = [str(line).replace("\n", "") for line in files.readlines()]
    except IOError:
        print "{}文件打开失败".format(file_name)
        exit()
    finally:
        if files:
            files.close()
            del files
    return result


def string_list(string):
    if not isinstance(string, str):
        raise TypeError("string_list函数必须要传入一个str类型的参数")
    temp_strings = string.split(",")
    result_string = []
    for temp_string in temp_strings:
        if str(temp_string).strip() != "" and not result_string.count(str(temp_string).strip()):
            result_string.append(temp_string)
    return result_string

if __name__ == "__main__":
    print_logo()
    if len(sys.argv) <= 1:
        print "{} -h".format(sys.argv[0])
        exit()
    args = help()
    targets, plugins, level, debug, headers = get_parserdata(args)
    try:
        task_schedule.main(targets, load_plugin.load_plugins(plugins), level, debug, headers)
    except PluginsNotFound, e:
        print str(e)
        exit()

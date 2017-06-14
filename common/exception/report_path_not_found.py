#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
@Author：W2n1ck
@Index：http://www.w2n1ck.com/
'''


class ReportPathNotFoundException(Exception):
    def __init__(self, path=None):
        Exception.__init__(self, "保存报告路径不能为空")
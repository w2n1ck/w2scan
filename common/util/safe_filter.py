#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
@Author：W2n1ck
@Index：http://www.w2n1ck.com/
'''

def check_traversal(name):
    if "../" not in name:
        return name
    name = name.replace("../","")
    name = check_traversal(name)
    return name

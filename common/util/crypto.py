#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
@Author：W2n1ck
@Index：http://www.w2n1ck.com/
'''
import hashlib


def md5_encrypt(str):
    m2 = hashlib.md5()
    m2.update(str)
    return m2.hexdigest()
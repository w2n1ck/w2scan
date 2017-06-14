#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
@Author：W2n1ck
@Index：http://www.w2n1ck.com/
'''
import os

BASEPATH = ''

def getplugspath(refresh=False):
    global BASEPATH
    if refresh:
        BASEPATH = None
    if BASEPATH:
        return BASEPATH
    #BASEPATH = os.path.abspath(__file__)
    BASEPATH = os.path.abspath(os.path.dirname(__file__))
    return BASEPATH
    #print BASEPATH


def get_modles():
    lsdir = os.listdir(getplugspath())
    dirs = [i for i in lsdir if os.path.isdir(os.path.join(getplugspath(), i))]
    for dir in dirs:
        print dir

if __name__ == "__main__":
    get_modles()
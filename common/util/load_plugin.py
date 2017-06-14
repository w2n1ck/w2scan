#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
@Author：W2n1ck
@Index：http://www.w2n1ck.com/
'''
import sys
sys.path.append("../..")
import os
import imp
from flask.plugins import plugin_config
from flask.common.util import safe_filter
from flask.common.exception.poc_exception import PluginsNotFound



def load_pyfiles(path):
    files = []
    try:
        temp_files = os.listdir(path)
        for file in temp_files:
            if file.endswith('.py') and file != '__init__.py':
                files.append(path + '/' + file)
    except Exception, e:
        raise PluginsNotFound(path)
    return files


def load_plugins_bypath(path=''):
    py_files = []
    path = plugin_config.getplugspath() + "/" + path
    try:
        py_files = load_pyfiles(path)
    except PluginsNotFound, e:
        raise PluginsNotFound(path)
    return py_files


def load_plugins(fct_model_name):
    model_names = []
    poclist = []
    if isinstance(fct_model_name, str):
        model_names.append(fct_model_name)
    elif isinstance(fct_model_name, list):
        model_names = fct_model_name
    for model_name in model_names:
        model_name = safe_filter.check_traversal(model_name)
        try:
            py_files = load_plugins_bypath(model_name)
            for plugin_file in py_files:
                poc = imp.load_source('Poc', plugin_file)
                poc = poc.Poc()
                poclist.append(poc)
        except PluginsNotFound, e:
            raise PluginsNotFound(model_name)
    return poclist

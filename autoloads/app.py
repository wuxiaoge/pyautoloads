#-*- coding:utf-8 -*-
import os
from autoloads import json_encode

class Tornado(object):

    format_funcs = {
        'string' : lambda s:s,
        'json' : json_encode,
    }
    handlers = []
    not_scan_file = ['__init__']

    def __new__(cls,*args,**kw):
        if not hasattr(cls,'instance'):
            cls.instance = object.__new__(Tornado,*args,**kw)
        return cls.instance

    def __call__(self):
        return Tornado.handlers

    def _get_scan_file(self,dirr):
        fileList = []
        for s in os.listdir(dirr):
            newDir = os.path.join(dirr,s)
            if os.path.isfile(newDir):
                fileDir = os.path.splitext(newDir)
                if (fileDir[1] == '.py'):
                    _file_name = fileDir[0]
                    if _file_name.startswith('./'):
                        _file_name = _file_name[2:]
                    _file_name = _file_name.split('/')
                    if not set(Tornado.not_scan_file) & set(_file_name):
                        _file_name = '.'.join(_file_name)
                        fileList.append(_file_name)
            elif os.path.isdir(newDir):
                fileList += self._get_scan_file(newDir)
        return fileList

    def scan(self,scan_dir):
        _scan_file_list = self._get_scan_file(scan_dir)
        for _scan_file in _scan_file_list:
            __import__(_scan_file)

    def route(self,path = '/',**kw):
        def _cls(cls):
            self.handlers.append((path,cls,kw))
            return cls
        return _cls

app = Tornado()


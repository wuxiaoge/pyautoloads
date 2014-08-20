#-*- coding:utf-8 -*-
import copy
from decimal import Decimal

def get_page_count(record_count,page_size):
    return int((record_count + page_size - 1) / page_size)

def get_record_index(page_index,page_size):
    return int((page_index - 1) * page_size)

class Parser(object):
    def parser(self):
        raise Exception("Parser's function(parser) is not implement")

    def __call__(self):
        return self.parser()

class BuildFilter(Parser):
    def __init__(self,entity):
        self._entity = entity

    def parser(self):
        if not self._entity: return []
        cls = self._entity.__class__
        if hasattr(cls,"filter_attr_dict") and cls.filter_attr_dict:
            filter_attr_dict = cls.filter_attr_dict
            filter_list = map(lambda x:filter_attr_dict[x](getattr(self._entity,x)) if getattr(self._entity,x) is not None else "",filter_attr_dict.keys())
        else:
            attrs = cls.__mapper__.columns.keys()
            filter_list = map(lambda x:getattr(cls,x)==getattr(self._entity,x) if getattr(self._entity,x) else "",attrs)
        return filter(lambda x:x,filter_list)

class RequestParser(Parser):
    parser_types = [int,float,Decimal]

    def __init__(self,cls,request):
        self.cls = cls
        self.request_arguments = copy.deepcopy(request.arguments)
        self.column_prefix = self.cls.__mapper_args__["column_prefix"]

    def parser(self):
        if not(self.cls) and not(self.request_arguments):
            return None
        args = {"%s%s" % (self.column_prefix,arg):self.request_arguments[arg] for arg in self.request_arguments}
        if hasattr(self.cls,"request_parser_attr_dict") and self.cls.request_parser_attr_dict:
            request_parser_attrs = self.cls.request_parser_attr_dict.keys()
            request_parserd_dict = {}
            for attr in request_parser_attrs:
                if args.has_key(attr):
                    request_parserd_dict[attr] = self.cls.request_parser_attr_dict[attr](args[attr][-1])
        else:
            attrs = dict(self.cls.__mapper__.columns.items())
            request_parserd_dict = {}
            for attr in args.keys():
                if attrs.has_key(attr):
                    py_type = attrs[attr].type.python_type
                    request_parserd_dict[attr] = py_type(args[attr][-1]) if py_type in self.__class__.parser_types else value
        return request_parserd_dict

class EntityParser(Parser):
    def __init__(self,entity,**attrs):
        self.entity = entity
        self.attrs = attrs

    def parser(self):
        if self.entity:
            for attr in self.attrs:
                if hasattr(self.entity,attr):
                    setattr(self.entity,attr,self.attrs[attr])
        return self.entity






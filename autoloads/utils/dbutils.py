#!usr/bin/env python
# coding: utf-8

import copy
from decimal import Decimal


def get_page_count(record_count, page_size):
    return int((record_count + page_size - 1) / page_size)


def get_record_index(page_index, page_size):
    return int((page_index - 1) * page_size)


class Parser(object):
    def parser(self):
        """在子类中定义实质的解析.
        """
        raise Exception("Parser's function(parser) is not implement")

    def __call__(self):
        """为子类的方法使用返回 'parser()' 结果.
        """
        return self.parser()


class BuildFilter(Parser):
    """从实体类的实例中生成过滤条件.
    """

    def __init__(self, entity):
        self._entity = entity

    def parser(self):
        if not self._entity:
            return []

        cls = self._entity.__class__
        if hasattr(cls, "filter_attr_dict") and cls.filter_attr_dict:
            filter_attr_dict = cls.filter_attr_dict
            filter_list = map(
                lambda x: filter_attr_dict[x](getattr(self._entity, x)) if getattr(self._entity, x) is not None else "",
                filter_attr_dict.keys())
        else:
            attributes = cls.columns().keys()
            filter_list = map(
                lambda x: getattr(cls, x) == getattr(self._entity, x) if getattr(self._entity, x) else "",
                attributes)

        return filter_list


class RequestParser(Parser):
    """在请求处理器中实体类解析.
    """
    parser_types = [int, float, Decimal]

    def __init__(self, cls, request):
        """
            :param cls:     实体类
            :param request: 页面处理器请求(self.request)

        在页面请求处理器中使用形式如下::

            class Test(BaseRequestHandler):
                def get(self):
                    from models import User
                    rp = RequestParser(User, self.request)
        """
        self.cls = cls
        self.request_arguments = copy.deepcopy(request.arguments)
        self.column_prefix = self.cls.column_prefix()

    def parser(self):
        if not self.cls and not self.request_arguments:
            return None

        # 从请求参数(request.arguments)的key/value中, 构建新的字典, key增加前缀.
        args = {"%s%s" % (self.column_prefix, arg): self.request_arguments[arg] for arg in self.request_arguments}

        request_parser_dict = {}
        if hasattr(self.cls, "request_parser_attr_dict") and self.cls.request_parser_attr_dict:
            # 如果实体类有该项, 并且该项的值为真.
            request_parser_attributes = self.cls.request_parser_attr_dict.keys()

            # 遍历实体类的request_parser_attr_dict属性集.
            # 如果有key存在与请求参数(request.arguments)则记录.
            for attr in request_parser_attributes:
                if attr in args:
                    request_parser_dict[attr] = self.cls.request_parser_attr_dict[attr](args[attr][-1])
        else:
            # 如果实体类无该项, 则以该实体类的全列.
            attributes = dict(self.cls.columns().items())
            for attr in args.keys():
                if attr in attributes:
                    # 获取数据库列的对应python类型.
                    py_type = attributes[attr].type.python_type
                    request_parser_dict[attr] = py_type(
                        args[attr][-1]) if py_type in self.__class__.parser_types else args[attr]

        return request_parser_dict


class EntityParser(Parser):
    """实体对象解析. 将一个字典key/value的值, 设置到该对象对应的key值上并返回给实体.
    """

    def __init__(self, entity, **_attributes):
        self.entity = entity
        self._attributes = _attributes

    def parser(self):
        if self.entity:
            for attr in self._attributes:
                if hasattr(self.entity, attr):
                    setattr(self.entity, attr, self._attributes[attr])
        return self.entity

#!usr/bin/env python
# coding: utf-8

from datetime import date, datetime
from types import ListType, DictType
from json import dumps
from decimal import Decimal


def json_data_encode(json_data):
    u"""可以序列化 datetime等多类型数据.

        :param json_data
    """
    def _any(data):
        if isinstance(data, ListType):
            return_data = _list(data)
        elif isinstance(data, DictType):
            return_data = _dict(data)
        elif isinstance(data, Decimal):
            return_data = str(data)
        elif isinstance(data, float):
            return_data = float(data)
        elif isinstance(data, datetime):
            return_data = data.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(data, date):
            return_data = data.strftime('%Y-%m-%d')
        else:
            return_data = data
        return return_data

    def _list(data):
        list_data = []
        for v in data:
            list_data.append(_any(v))
        return list_data

    def _dict(data):
        dict_data = {}
        for k, v in data.items():
            dict_data[k] = _any(v)
        return dict_data

    ret = _any(json_data)
    return dumps(ret, cls=None, ensure_ascii=False, indent=4)

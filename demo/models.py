#!usr/bin/env python
# coding: utf-8

from autoloads import Entity, EntityHelper
from config import my_db_models

# 根据自动加载的数据库models获取对应的model
user = my_db_models('table_user')


class User(Entity, EntityHelper):
    # 供BuildFilter使用, 过滤条件的生成字典, 根据该字典生成对应的过滤条件.
    filter_attr_dict = dict(
        id=lambda x: User.id == int(x),
    )

    # 供RequestParser使用, 请求参数字典的生成处理, 请求参数根据该字典生成对应model的属性.
    request_parser_attr_dict = dict(
        id=lambda x: int(x),
    )

    # 返回需要生成json的字段, 返回None则包含所有字段.
    def json_decode_attrs(self):
        return ["id"]

    # 生成json时, 对应字段的处理方式.
    def json_attr_parser_funcs(self):
        return dict(
            id=int,
        )

    def __init__(self, **kargs):
        Entity.__init__(self, **kargs)

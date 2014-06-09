#-*- coding:utf-8 -*-
from autoloads.utils.dbhelper import DBEntityOper
from autoloads import json_encode

class Entity(object):
    db_oper_cls = DBEntityOper

    def __init__(self,**kargs):
        map(lambda x:setattr(self,"%s" % (x),kargs[x]),kargs)

    def save(self):
        self.cls.add(self)

    def json_decode_attrs(self):
        """需要json化的对象属性"""
        pass

    def json_attr_parser_funcs(self):
        """需要进行数据处理的属性方法"""
        pass

    def json(self):
        column_prefix_len = len(self.__class__.__mapper_args__["column_prefix"])
        _attrs = self.json_decode_attrs() or self.__mapper__.columns.keys()
        _parser_funcs = self.json_attr_parser_funcs() or {}
        attr_items = [(_attr,_parser_funcs[_attr](getattr(self,_attr)) if _parser_funcs.has_key(_attr) else getattr(self,_attr)) for _attr in _attrs]
        attr_items = map(lambda x:(x[0][column_prefix_len:],x[1] if isinstance(x[1],(list,dict)) else unicode(x[1])),attr_items)
        attr_dict = dict(attr_items)
        return attr_dict

    def __str__(self):
        attr_dict = self.json()
        return json_encode(attr_dict)

    def __repr__(self):
        return self.__str__()

class EntityOper(object):

    @classmethod
    def add(cls,entity):
        _db_oper = cls.db_oper_cls(cls)
        _db_oper.add(entity)
        _db_oper.commit()
        _db_oper.close()

    @classmethod
    def add_all(cls,entitys):
        _db_oper = cls.db_oper_cls(cls)
        _db_oper.add_all(entitys)
        _db_oper.commit()
        _db_oper.close()

    @classmethod
    def delete(cls,entity):
        _db_oper = cls.db_oper_cls(cls)
        _db_oper.delete(entity)
        _db_oper.commit()
        _db_oper.close()

    @classmethod
    def delete_by_where(cls,*where):
        _db_oper = cls.db_oper_cls(cls,where)
        _db_oper.delete_all()
        _db_oper.commit()
        _db_oper.close()

    @classmethod
    def update_by_where(cls,*where,**attrs):
        _db_oper = cls.db_oper_cls(cls,where)
        _db_oper.update_all(**attrs)
        _db_oper.commit()
        _db_oper.close()

    @classmethod
    def get_scalar_by_where(cls,query_expr,*where):
        _db_oper = cls.db_oper_cls(cls,where)
        _count = _db_oper.get_scalar(query_expr)
        _db_oper.commit()
        _db_oper.close()
        return _count

    @classmethod
    def get_first_by_where(cls,*where):
        _db_oper = cls.db_oper_cls(cls,where)
        _entity = _db_oper.get_first()
        _db_oper.commit()
        _db_oper.close()
        return _entity

    @classmethod
    def get_first_order_by_where(cls,order_by_cols,*where):
        _db_oper = cls.db_oper_cls(cls,where,order_by_cols)
        _entity = _db_oper.get_first_order_by()
        _db_oper.commit()
        _db_oper.close()
        return _entity

    @classmethod
    def get_all_by_where(cls,recordindex,pagesize,*where):
        _db_oper = cls.db_oper_cls(cls,where)
        _entitys = _db_oper.get_all(recordindex,pagesize)
        _db_oper.commit()
        _db_oper.close()
        return _entitys

    @classmethod
    def get_all_order_by_where(cls,recordindex,pagesize,order_by_cols,*where):
        _db_oper = cls.db_oper_cls(cls,where,order_by_cols)
        _entitys = _db_oper.get_all_order_by(recordindex,pagesize)
        _db_oper.commit()
        _db_oper.close()
        return _entitys






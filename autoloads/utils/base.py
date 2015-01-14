#-*- coding:utf-8 -*-
from autoloads.utils.dbhelper import DBEntityOper
from autoloads import json_encode

class Entity(object):
    db_oper_cls = DBEntityOper

    def __init__(self,**kargs):
        map(lambda x:setattr(self,"%s" % (x),kargs[x]),kargs)

    def save(self):
        self.__class__.add(self)

    def json_decode_attrs(self):
        """需要json化的对象属性"""
        pass

    def json_attr_parser_funcs(self):
        """需要进行数据处理的属性方法"""
        pass

    @classmethod
    def column_prefix(cls):
        return cls.__mapper_args__["column_prefix"]

    @classmethod
    def columns(cls):
        return cls.__mapper__.columns

    def json(self):
        column_prefix_len = len(self.__class__.column_prefix())
        _attrs = self.json_decode_attrs() or self.__class__.columns().keys()
        _parser_funcs = self.json_attr_parser_funcs() or {}
        attr_items = [(_attr,_parser_funcs[_attr](getattr(self,_attr)) if _parser_funcs.has_key(_attr) else getattr(self,_attr)) for _attr in _attrs]
        attr_items = map(lambda x:(x[0][column_prefix_len:],x[1]),attr_items)
        attr_dict = dict(attr_items)
        return attr_dict

    def __str__(self):
        attr_dict = self.json()
        return json_encode(attr_dict)

    def __repr__(self):
        return self.__str__()

class EntityOper(object):

    @classmethod
    def add(cls,entity,refresh=True):
        _db_oper = cls.db_oper_cls(entity_cls = cls)
        try:
            _db_oper.add(entity)
            if refresh:
                _db_oper.flush()
                _db_oper.refresh(entity)
            _db_oper.commit()
        except Exception,ex:
            _db_oper.rollback()
            raise ex
        finally:
            _db_oper.close()

    @classmethod
    def add_all(cls,entitys,refresh=True):
        _db_oper = cls.db_oper_cls(entity_cls = cls)
        try:
            _db_oper.add_all(entitys)
            if refresh:
                _db_oper.flush()
                map(lambda x:_db_oper.refresh(x),entitys)
            _db_oper.commit()
        except Exception,ex:
            _db_oper.rollback()
            raise ex
        finally:
            _db_oper.close()

    @classmethod
    def delete(cls,entity):
        _db_oper = cls.db_oper_cls(entity_cls = cls)
        try:
            _db_oper.delete(entity)
            _db_oper.commit()
        except Exception,ex:
            _db_oper.rollback()
            raise ex
        finally:
            _db_oper.close()

    @classmethod
    def delete_by_where(cls,wheres = None):
        _db_oper = cls.db_oper_cls(entity_cls = cls,
                                   wheres = wheres)
        try:
            _db_oper.delete_all()
            _db_oper.commit()
        except Exception,ex:
            _db_oper.rollback()
            raise ex
        finally:
            _db_oper.close()

    @classmethod
    def update_by_where(cls,wheres = None,**attrs):
        _db_oper = cls.db_oper_cls(entity_cls = cls,
                                   wheres = wheres)
        try:
            _db_oper.update_all(**attrs)
            _db_oper.commit()
        except Exception,ex:
            _db_oper.rollback()
            raise ex
        finally:
            _db_oper.close()

    @classmethod
    def get_scalar_by_where(cls,query_expr,wheres = None):
        _db_oper = cls.db_oper_cls(entity_cls = cls,
                                   wheres = wheres)
        _count = _db_oper.get_scalar(query_expr)
        _db_oper.commit()
        _db_oper.close()
        return _count

    @classmethod
    def get_statistics_by_group(cls,recordindex,pagesize,group_by_list,order_by_cols = None,wheres = None,cols = None):
        _db_oper = cls.db_oper_cls(entity_cls = cls,
                                   entity_cols = cols,
                                   wheres = wheres,
                                   order_by_cols = order_by_cols)
        _statistics = _db_oper.get_statistics_by_group(group_by_list,recordindex,pagesize)
        _db_oper.commit()
        _db_oper.close()
        return _statistics

    @classmethod
    def get_first_by_where(cls,wheres = None,cols = None):
        _db_oper = cls.db_oper_cls(entity_cls = cls,
                                   entity_cols = cols,
                                   wheres = wheres)
        _entity = _db_oper.get_first()
        _db_oper.commit()
        _db_oper.close()
        return _entity

    @classmethod
    def get_first_order_by_where(cls,order_by_cols,wheres = None,cols = None):
        _db_oper = cls.db_oper_cls(entity_cls = cls,
                                   entity_cols = cols,
                                   wheres = wheres,
                                   order_by_cols = order_by_cols)
        _entity = _db_oper.get_first_order_by()
        _db_oper.commit()
        _db_oper.close()
        return _entity

    @classmethod
    def get_all_by_where(cls,recordindex,pagesize,wheres = None,cols = None):
        _db_oper = cls.db_oper_cls(entity_cls = cls,
                                   entity_cols = cols,
                                   wheres = wheres)
        _entitys = _db_oper.get_all(recordindex,pagesize)
        _db_oper.commit()
        _db_oper.close()
        return _entitys

    @classmethod
    def get_all_order_by_where(cls,recordindex,pagesize,order_by_cols,wheres = None,cols = None):
        _db_oper = cls.db_oper_cls(entity_cls = cls,
                                   entity_cols = cols,
                                   wheres = wheres,
                                   order_by_cols = order_by_cols)
        _entitys = _db_oper.get_all_order_by(recordindex,pagesize)
        _db_oper.commit()
        _db_oper.close()
        return _entitys






#-*- coding:utf-8 -*-
from autoloads.utils.dbpipe import sql_query
from autoloads.utils.dbpipe import query_filter
from autoloads.utils.dbpipe import offset
from autoloads.utils.dbpipe import limit
from autoloads.utils.dbpipe import first
from autoloads.utils.dbpipe import all
from autoloads.utils.dbpipe import scalar
from autoloads.utils.dbpipe import order_by
from autoloads.utils.dbpipe import group_by

from autoloads.utils.dbpipe import update
from autoloads.utils.dbpipe import add
from autoloads.utils.dbpipe import add_all
from autoloads.utils.dbpipe import delete
from autoloads.utils.dbpipe import query_delete

from autoloads.utils.dbpipe import commit
from autoloads.utils.dbpipe import rollback
from autoloads.utils.dbpipe import close

class DBEntityOper(object):
    def __init__(self,entity_cls,entity_cols=None,wheres = None,order_by_cols = None):
        self._entity_cls = entity_cls
        self._entity_cols = entity_cols or [entity_cls]
        self._dbsession = self._entity_cls.db_session_pool()
        self._where = wheres or []
        self._order_by_cols = order_by_cols or []

    def commit(self):
        return self._dbsession | commit

    def rollback(self):
        return self._dbsession | rollback

    def close(self):
        return self._dbsession | close

    def get_query(self,*cols):
        return self._dbsession | sql_query(*cols) | query_filter(*self._where)

    def get_first(self):
        return self.get_query(*self._entity_cols) | first

    def get_first_order_by(self):
        return self.get_query(*self._entity_cols) | order_by(*self._order_by_cols) | first

    def get_all(self,record_index,record_size):
        return self.get_query(*self._entity_cols) | offset(record_index) | limit(record_size) | all

    def get_all_order_by(self,record_index,record_size):
        return self.get_query(*self._entity_cols) | order_by(*self._order_by_cols) | offset(record_index) | limit(record_size) | all

    def get_scalar(self,query_expr):
        return self.get_query(query_expr) | scalar

    def add(self,entity):
        return self._dbsession | add(entity)

    def add_all(self,entitys):
        return self._dbsession | add_all(entitys)

    def delete(self,entity):
        return self._dbsession | delete(entity)

    def delete_all(self):
        return self.get_query(*self._entity_cols) | query_delete

    def update_all(self,**attrs):
        return self.get_query(*self._entity_cols) | update(attrs)




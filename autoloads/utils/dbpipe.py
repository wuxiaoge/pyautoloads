#-*- coding:utf-8 -*-
from pipe import Pipe

#======================query=========================
@Pipe
def sql_query(dbsession,*cols):
    return dbsession.query(*cols)

@Pipe
def query_filter(query,*where):
    return query.filter(*where)

@Pipe
def offset(query,record_index):
    return query.offset(record_index)

@Pipe
def limit(query,record_size):
    return query.limit(record_size)

@Pipe
def first(query):
    return query.first()

@Pipe
def all(query):
    return query.all()

@Pipe
def scalar(query):
    return query.scalar()

@Pipe
def order_by(query,*order_by_cols):
    return query.order_by(*order_by_cols)

@Pipe
def group_by(query,*group_by_cols):
    return query.group_by(*group_by_cols)

#=====================update=========================
@Pipe
def update(query,**attrs):
    return query.update(attrs,synchronize_session="fetch")

@Pipe
def add(dbsession,entity):
    return dbsession.add(entity)

@Pipe
def add_all(dbsession,entitys):
    return dbsession.add_all(entitys)

@Pipe
def delete(dbsession,entity):
    return dbsession.delete(entity)

@Pipe
def query_delete(query):
    return query.delete(synchronize_session="fetch")

@Pipe
def refresh(dbsession,entity):
    return dbsession.refresh(entity)

@Pipe
def flush(dbsession):
    return dbsession.flush()

#===================transaction======================
@Pipe
def commit(dbsession):
    return dbsession.commit()

@Pipe
def rollback(dbsession):
    return dbsession.rollback()

@Pipe
def close(dbsession):
    return dbsession.close()

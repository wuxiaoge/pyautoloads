#-*- coding:utf-8 -*-

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import Table
from new import classobj


class _Models(object):

    def __init__(self,host,echo=False,pool_recycle=7200,table_names=None,column_prefix='_',schema=None,expire_on_commit=False):
        self.models = {}
        self.expire_on_commit = expire_on_commit
        self.schema = schema
        self.host = host
        self.echo = echo
        self.pool_recycle = pool_recycle
        self.column_prefix = column_prefix
        self.get_engine()
        self.get_base()
        if table_names is None:
            self.table_names = self.engine.table_names()
        else:
            self.table_names = table_names
        for _tablename in self.table_names:
            _table_name = '{0}'.format(_tablename)
            self.models[_table_name] = self._generate_model(_table_name,self.engine)

    def __call__(self,tablename=None):
        if tablename is None:
            return self.models
        return self.models[tablename]

    def get_engine(self):
        if not hasattr(self,'engine'):
            self.engine = create_engine(self.host,echo=self.echo,pool_recycle=self.pool_recycle)
        return self.engine

    def get_db_session_pool(self):
        if not hasattr(self,'db_session_pool'):
            self.db_session_pool = sessionmaker(expire_on_commit=self.expire_on_commit)
            self.db_session_pool.configure(bind=self.engine)
        return self.db_session_pool

    def get_base(self):
        if not hasattr(self,'base'):
            self.base = declarative_base()
        return self.base

    def _generate_model(self,tablename,engine,model_name=None):
        if model_name is None:
            model_name = tablename
        _table = Table(tablename,self.base.metadata,autoload=True,autoload_with=self.engine,schema=self.schema)
        _model = classobj(model_name, (self.base,), {'__table__' : _table, 
                                                     '__mapper_args__' : {'column_prefix' : self.column_prefix},
                                                     'db_session_pool' : self.get_db_session_pool()}) 
        return _model

class Models(object):
    _models = {}

    def __new__(cls,host,port,user,passwd,database,tables=None,charset='utf8',echo=False,pool_recycle=7200,column_prefix='_',schema=None):
        if database not in cls._models:
            _connection_str = 'mysql+pymysql://{0}:{1}@{2}:{3}/{4}?charset={5}'.format(user,passwd,host,port,database,charset)
            cls._models[database] = _Models(_connection_str,echo=echo,pool_recycle=pool_recycle,table_names=tables,column_prefix=column_prefix,schema=schema)
        return cls._models[database]

    @classmethod
    def get_models_by_database(cls,database):
        return cls._models[database]

#column_prefix参数表示在列名前加上该参数的值来作为该model的属性
#若tables为None则Models将会吧绑定的数据库中的所有表都生成对应的model
#Models根据绑定的数据库生成的modol你指定的或全部生成，所以返回的_models是多个model对象的字典，表名为key，对应的value则是它的model对象
#_models = Models('localhost',3306,'root','','you_db',tables=['you_table1',...],echo=True,column_prefix='attr_')
#_engine = _models.get_engine() #获取生成该model的数据库引擎
#DBSession = sessionmaker(bind=_engine) #生成DBSession
#you_table1 = _models('you_table1') #根据表明获取对应的model，若不传入表名或存入None则返回该数据库中的表所对应的所有model
#class YouTable1(you_table1): pass #因人而异，上一行返回的sku本身就是一个class，该处Sku继承sku，下面代码使用了Sku，这样可以增强可读性，一眼可看出Sku是个class，是个model
#
#if __name__ == '__main__':
#    dbsession = DBSession()
#    _infos = dbsession.query(YouTable1).order_by(YouTable1.attr_id.desc()).limit(5).all() #该model设置了属性前缀，所以所有的属性都是前缀加上列名
#    _info_list = []
#    for _info in _infos:
#        _info_list.append({'id':_info.attr_id,'col1':_info.attr_col1,'col2':_info.attr_col2}) #同上
#    print _info_list
#    dbsession.close()
#
#以上Models工具类采用的是单例模式，这样就不用担心在多出使用时会产生重复的model,可避免占用多余的数据库链接


#!usr/bin/env python
# coding: utf-8

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import Table
from new import classobj


class _Models(object):
    def __init__(self, host, echo=False, pool_recycle=7200,
                 table_names=None, column_prefix='_', schema=None, expire_on_commit=False):
        """
            :param host:                连接地址
            :param echo:                执行过程是否输出SQL
            :param schema:              所属schema
            :param table_names:         表名
            :param pool_recycle:        数据库连接池重连时间
            :param column_prefix:       Model的属性前缀
            :param expire_on_commit:    是否提交后失效, SQLAlchemy session的机制.

        注意: 若table_names为None则Models将会把绑定的数据库中的所有表都生成对应的model.
        """

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
        for _table_ in self.table_names:
            _table_name = '{0}'.format(_table_)
            self.models[_table_name] = self._generate_model(_table_name)

    def __call__(self, table_name=None):
        if table_name is None:
            return self.models
        return self.models[table_name]

    def get_engine(self):
        """获取生成该model的数据库引擎.
        """

        if not hasattr(self, 'engine'):
            self.engine = create_engine(self.host, echo=self.echo, pool_recycle=self.pool_recycle)
        return self.engine

    def get_db_session_pool(self):
        """获取生成该model的数据连接.
        """

        if not hasattr(self, 'db_session_pool'):
            self.db_session_pool = sessionmaker(expire_on_commit=self.expire_on_commit)
            self.db_session_pool.configure(bind=self.engine)

        return self.db_session_pool

    def get_base(self):
        if not hasattr(self, 'base'):
            self.base = declarative_base()
        return self.base

    def _generate_model(self, table_name, model_name=None):
        if model_name is None:
            model_name = table_name

        _table = Table(table_name, self.base.metadata,
                       autoload=True, autoload_with=self.engine, schema=self.schema)
        _model = classobj(model_name, (self.base,),
                          {'__table__': _table,
                           '__mapper_args__': {'column_prefix': self.column_prefix},
                           'db_session_pool': self.get_db_session_pool()})
        return _model


class Models(object):
    _models = {}

    def __new__(cls, host, port, user, passwd,
                database, tables=None, charset='utf8', echo=False,
                pool_recycle=7200, column_prefix='_', schema=None):
        """
            :param host:        连接地址
            :param port:        连接端口
            :param user:        账户
            :param passwd:      密码

            :param database:    数据库
            :param tables:      表名
            :param charset:     连接编码

            :param echo:            执行过程是否输出SQL
            :param pool_recycle:    数据库连接池重连时间
            :param column_prefix:   Model的属性前缀
            :param schema:          所属schema

            注意: 若tables为None则Models将会把绑定的数据库中的所有表都生成对应的model.
        """

        if database not in cls._models:
            _connection_str = 'mysql+pymysql://{0}:{1}@{2}:{3}/{4}?charset={5}'.format(
                user, passwd, host, port, database, charset)

            cls._models[database] = _Models(_connection_str, echo=echo,
                                            pool_recycle=pool_recycle,
                                            table_names=tables,
                                            column_prefix=column_prefix,
                                            schema=schema)
        return cls._models[database]

    @classmethod
    def get_models_by_database(cls, database):
        return cls._models[database]

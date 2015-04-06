#!usr/bin/env python
# coding: utf-8

import functools
from autoloads import Models

# 修改你自己的数据库连接参数
MYSQL_CONFIG = dict(
    host="localhost",
    port=3306,
    user="root",
    password="123456",
    charset="utf8",
)

# 定义你数据库里及对应的表
MYSQL_DATABASES_TABLES = dict(
    test_db=["table_one", "table_two", "table_user"],
)


def generate_models(mysql_config, databases_config, database_name,
                    db_pool_recycle=60, echo=False, column_prefix='_'):
    """"从数据库表生成模型

        :param mysql_config:        MySQL配置
        :param databases_config:    数据库配置
        :param database_name:　      数据库名称
        :param db_pool_recycle:     数据库连接池
        :param echo:                回显SQL语句
        :param column_prefix:       属性(列)前缀
    """

    _host = mysql_config['host']
    _port = mysql_config['port']
    _user = mysql_config['user']
    _password = mysql_config['password']
    _database = database_name
    _charset = mysql_config['charset']
    _tables = databases_config[_database]
    _models = Models(host=_host,
                     port=_port,
                     user=_user,
                     password=_password,
                     database=_database,
                     tables=_tables,
                     charset=_charset,
                     echo=echo,
                     pool_recycle=db_pool_recycle,
                     column_prefix=column_prefix,
                     schema=_database)
    return _models


generate_models = functools.partial(generate_models, MYSQL_CONFIG, MYSQL_DATABASES_TABLES)

# 按数据库名称生成该数据库对应配置的表的model(table_one,table_two)
my_db_models = generate_models("test_db")

if __name__ == '__main__':

    # 获得表table_one对应的Model
    table_one = my_db_models("table_one")

    # 使用Model的db_session_pool方法获取连接
    db_session = table_one.db_session_pool()

    table_one_info = db_session.query(table_one).filter().first()
    if table_one_info:
        table_one_info.name = "test"
        table_one_info.text = "test_text"
    else:
        pass

    db_session.add(table_one_info)
    db_session.commit()
    db_session.close()
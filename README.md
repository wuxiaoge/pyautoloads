pyautoloads
====

**pyautoloads** 是tornado web 简易开发工具包,支持数据库models自动生成加载,handler采用装饰器方式配置,并自动扫描handler并加载.
使用方式如下:
```python
import functools

MYSQL_CONFIG = dict(
    host = "localhost",
    port = 3306,
    user = "root",
    passwd = "",
    charset = "utf8",
)

MYSQL_DATABASES_TABLES = dict(
    your_db = ["your_table1","your_table2"],    
)     

def generate_models(mysql_config,databases_config,database_name,db_pool_recycle=60, \
                    echo=False,column_prefix=''):
    _host     = mysql_config['host']
    _port     = mysql_config['port']
    _user     = mysql_config['user']
    _passwd   = mysql_config['passwd']
    _database = database_name
    _charset  = mysql_config['charset']
    _tables   = databases_config[_database]
    _models   =  Models( host         = _host,
                         port         = _port,
                         user         = _user,
                         passwd       = _passwd,
                         database     = _database,
                         tables       = _tables,
                         charset      = _charset,
                         echo         = echo,
                         pool_recycle = db_pool_recycle,
                         column_prefix = column_prefix,
                         schema = _database
    )   
    return _models

generate_models = functools.partial(generate_models,MYSQL_CONFIG,MYSQL_DATABASES_TABLES)
#按数据库名称生成该数据库对应配置的表的model(your_table1,your_table2)
your_db_models = generate_models("your_db") 
#获得表your_table1对应的model
your_model1 = your_db_models("your_table1")
#获得表your_table2对应的model
your_model2 = your_db_models("your_table2")
#使用model的db_session_pool方法获取dbsession
dbsession = your_model1.db_session_pool()
your_model1_infos = dbsession.query(your_model1).filter(...).all()
```

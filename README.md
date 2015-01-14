pyautoloads
====

**pyautoloads** 是tornado web 简易开发工具包,支持数据库models自动生成加载,handler采用装饰器方式配置,并自动扫描handler并加载.
使用方式如下:
(数据库自动加载绑定实体及其使用)
```python
import functools
from autoloads import Models

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
your_model1_infos = dbsession.query(your_model1).filter(...).first()
your_model1_infos.attr1 = "test"
dbsession.add(your_model1_infos)
dbsession.commit()
dbsession.close()
```
(handler自动加载及简单请求参数处理)
models.py
```python
from models import Entity #包含实体对象的简单操作
from models import EntityOper #数据库操作封装

user = db_models('user') #根据自动加载的数据库models获取对应的model
class User(classuser,Entity,EntityOper):
    filter_attr_dict = dict( #过滤条件的生成字典,根据该字典生成对应的过滤条件
        id = lambda x:User.id==int(x),
    )   

    request_parser_attr_dict = dict( #请求参数字典的生成处理字典,请求参数根据该字典生成对应model的属性字典
        id = lambda x:int(x),
    )   

    def json_decode_attrs(self): #返回需要生成json的字段,返回None则包含所有字段
        return ["id"]

    def json_attr_parser_funcs(self): #生成json时,对应字段的处理方式
        return dict(
            id = int,
        )   

    def __init__(self,**kargs):
        Entity.__init__(self,**kargs)
```
review.py
```python
from autoloads import app 
from autoloads import BaseRequestHandler
from autoloads.utils.dbutils import BuildFilter
from autoloads.utils.dbutils import RequestParser
from models.user import User

@app.route('/test')
class Test(BaseRequestHandler):
    def get(self):
        rp = RequestParser(User,self.request) #从request中获取参数,并对应User实体类生成对应的dict
        cu = User(**rp()) #将根据request生成的dict作为参数传入User实体中
        bf = BuildFilter(cu) #根据User实体类的实例cu生成过滤条件
        cus = User.get_all_by_where(0,10,*bf()) #根据条件查询实例
        cus = [cu.json() for cu in cus] #将实例全部转换成字典
        result = self.build_response_json(success=True,message=cus) #创建固定格式的返回数据结构
        self.write(result)
```

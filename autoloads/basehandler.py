#!usr/bin/env python
# coding: utf-8

import tornado.web
from mako.lookup import TemplateLookup
from tornado.escape import json_encode


class _Template(object):
    """对第三方模板引擎的封装.
    """

    def __new__(cls, directories, module_directory, output_encoding='utf-8', cache_enabled=False):
        """在实例化时创建 "_lookup" 属性.

            :param directories:         mako模板文件存储位置, 列表形式: ['./templates']
            :param module_directory:    mako模板系统编译后py文件位置(缓冲目录)
            :param output_encoding:     输出字符串的编码
        """

        if not hasattr(cls, '_instance'):
            cls._instance = object.__new__(cls)
            cls._instance._init_template(directories, module_directory, output_encoding, cache_enabled)

        return cls._instance

    def _init_template(self, directories, module_directory, output_encoding, cache_enabled):
        """创建实例 "_lookup" 属性.

            :param directories:         mako模板文件存储位置, 列表形式: ['./templates']
            :param module_directory:    mako模板系统编译后py文件位置(缓冲目录)
            :param output_encoding:     输出字符串的编码
        """

        self._lookup = TemplateLookup(directories=directories,
                                      module_directory=module_directory,
                                      output_encoding=output_encoding,
                                      cache_enabled=cache_enabled)

    def render_template(self, template_name, **kwargs):
        """使用指定数据, 渲染指定模板.
        """
        _template = self._lookup.get_template(template_name)
        return _template.render(**kwargs)


class HttpRequestHandler(tornado.web.RequestHandler):
    """实现模板的渲染的类.
    """

    def getParameter(self, key, default_value=None):
        return self.get_argument(key, default_value)

    def prepare(self):
        """装载Application配置数据, 完成'模板引擎的封装类'的初始化.
        """
        _directories = self.settings.get('directories', ['./templates'])
        _module_directory = self.settings.get('module_directory', './templates_modules')
        _output_encoding = self.settings.get('output_encoding', 'utf-8')
        _cache_enabled = self.settings.get('cache_enabled', False)

        self._template = _Template(directories=_directories,
                                   module_directory=_module_directory,
                                   output_encoding=_output_encoding,
                                   cache_enabled=_cache_enabled)

    def render_template(self, template_name, **kwargs):
        """使用指定数据, 渲染指定模板.
        """
        return self._template.render_template(template_name, **kwargs)

    @staticmethod
    def response_json(**kwargs):
        return json_encode(kwargs)

    # 为兼容之前使用此组件的老项目
    build_response_json = response_json


class BaseRequestHandler(HttpRequestHandler):
    """在实质的页面处理器中继承它.
    """
    pass

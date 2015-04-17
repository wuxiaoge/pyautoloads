#-*- coding:utf-8 -*-
import tornado.web
from mako.lookup import TemplateLookup
from autoloads import json_encode

class _Template(object):

    def __new__(cls,directories,module_directory,output_encoding='utf-8',cache_enabled = False):
        if not hasattr(cls,'_instance'):
            cls._instance = object.__new__(cls)
            cls._instance._init_template(directories,module_directory,output_encoding,cache_enabled)
        return cls._instance

    def _init_template(self,directories,module_directory,output_encoding,cache_enabled):
        self._lookup = TemplateLookup(directories=directories, module_directory=module_directory, 
                                      output_encoding=output_encoding,cache_enabled=cache_enabled)

    def render_template(self,template_name,**kwargs):
        _template = self._lookup.get_template(template_name)
        return _template.render(**kwargs)

class HTTPRequestHandler(tornado.web.RequestHandler):

    def getParameter(self,key,default_value=None):
        return self.get_argument(key,default_value)

    def prepare(self):
        _directories      = self.settings.get('directories',['./templates'])
        _module_directory = self.settings.get('module_directory','./templates_modules')
        _output_encoding  = self.settings.get('output_encoding','utf-8')
        _cache_enabled    = self.settings.get('cache_enabled',False)
        self._template    = _Template(directories=_directories, module_directory=_module_directory, 
                                      output_encoding=_output_encoding, cache_enabled=_cache_enabled)

    def render_template(self,template_name,**kwargs):
        return self._template.render_template(template_name,**kwargs)

    def build_response_json(self,**kwargs):
        return json_encode(kwargs)

class BaseRequestHandler(HTTPRequestHandler):
    pass

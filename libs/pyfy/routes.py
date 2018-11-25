from pyparams_validator import types
from flask import render_template
from flask import  request

import os
__routes__ = {}
class __route_wrapper__(object):
    def __init__(self,data):
        self.name = ""
        from . import settings
        find_apps = [x for x in settings.list_of_apps if data.file.find(x["dir"])>-1]
        if find_apps.__len__()>0:
            self.host = find_apps[0]["host"]
            self.dir  = find_apps[0]["dir"]
            self.app_config = find_apps[0]
            self.app_config["owner"] = self
        self.__flask_app__ = settings.app
        self.url = data.url
        self.file = data.file
        self.template = data.template




    def wrapper(self,*args,**kwargs):
        if self.host!="":
            @self.__flask_app__.route("/"+self.host+self.url)
            def exec_route():
                from libs.pyfy import settings
                setattr(request,"excutor",self)
                data = args[0]()
                if data == None:
                    data = {}
                return render_template("/".join([self.app_config["rel_dir"],"views",self.template]),**data)
        else:
            @self.__flask_app__.route (self.url)
            def exec_route():
                from libs.pyfy import settings
                setattr (request, "excutor", self)
                data = args[0] ()
                if data == None:
                    data = {}
                return render_template ("/".join ([self.app_config["rel_dir"], "views", self.template]), **data)

@types(
    file=(str,True),
    url=(str,True),
    template=(str,True)
)
def route(data):
    ret = __route_wrapper__(data)
    return ret.wrapper
from pyparams_validator import types
from flask import render_template
from flask import  request
import models
import os
__routes__ = {}
class __route_wrapper__(object):
    def __init__(self,data):
        self.name = ""
        self.login_url =""
        self.rel_dir = ""
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

            def exec_route():

                model = models.model(self)
                data = models.dmobject()
                if request.method == "POST":
                    data =models.dmobject(request.form.to_dict())

                if hasattr(self.app_config["mdl"],"auth"):
                    if request.path !="/"+self.host+"/"+self.app_config["login_url"] and \
                            (not self.app_config["mdl"].auth()):
                        from flask import redirect
                        return redirect(self.host+"/"+self.app_config["login_url"])

                from libs.pyfy import settings
                setattr(request,"excutor",self)

                ret = args[0](model,data)
                model.set_data(data)
                if ret == None:
                    return render_template("/".join([self.app_config["rel_dir"],"views",self.template]),**model.__dict__)
                else:
                    return ret

            exec_route.func_name = self.app_config["rel_dir"].replace ("/", "_") + "_" + args[0].func_name
            self.__flask_app__.add_url_rule (
                "/" + self.host + self.url,
                view_func= exec_route,
                methods=["GET","POST"]
            )
        else:

            def exec_route():
                model = models.model (self)
                data = models.dmobject ()
                if request.method == "POST":
                    data = models.dmobject (request.form.to_dict ())
                if hasattr(self.app_config["mdl"],"auth"):
                    if not self.app_config["mdl"].auth():
                        from flask import redirect
                        return redirect("/"+self.login_url)
                from libs.pyfy import settings
                setattr (request, "excutor", self)
                ret = args[0] (model,data)
                model.set_data (data)
                if ret == None:
                    return render_template ("/".join ([self.app_config["rel_dir"], "views", self.template]),**model)
                else:
                    return ret

            exec_route.func_name = self.app_config["rel_dir"].replace ("/", "_") + "_" + args[0].func_name
            self.__flask_app__.add_url_rule (
                self.url,
                view_func=exec_route,
                methods=["GET", "POST"]
            )

@types(
    file=(str,True),
    url=(str,True),
    template=(str,True)
)
def route(data):
    ret = __route_wrapper__(data)
    return ret.wrapper
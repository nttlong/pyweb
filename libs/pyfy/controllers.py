from flask import request
from pyparams_validator import types
import models
from flask import render_template

class Controller(object):
    @property
    def absUrl(self):
        from flask import request
        return request.url.split("://")[0]+"://"+request.host
    @property
    def appUrl(self):
        from flask import request
        return self.absUrl+"/"+self.excutor.host
    @property
    def static(self):
        return self.absUrl + "/" + self.excutor.host+"/static"
    @property
    def language(self):
        from flask import session
        return session.get("language","en")
    @property
    def appDir(self):
        from . import settings
        from os.path import relpath
        import os
        return relpath(self.excutor.dir,settings.WORKING_DIR).replace(os.sep,"/")
    @property
    def appDirViews(self):
        return self.appDir+"/views"









    @property
    def request(self):
        from flask import request
        return request
    @property
    def session(self):
        from flask import session
        return session
    def redirect(self,url):
        from flask import redirect as rd
        return rd(url)
def __render__(template_dir,fileName,data):
    import os
    import jinja2
    templateLoader = jinja2.FileSystemLoader(searchpath=template_dir)
    templateEnv = jinja2.Environment(
        loader=templateLoader,
        variable_end_string="}",
        variable_start_string="${"

    )
    TEMPLATE_FILE = fileName
    template = templateEnv.get_template(TEMPLATE_FILE)
    outputText = template.render(**data.__dict__)  # this is where to put args to the template renderer
    return outputText
class __controller_wrapper__(object):
    def __init__(self,data):
        from . import settings
        self.__flask_app__ = settings.app
        find_apps = [x for x in settings.list_of_apps if data.file.find (x["dir"]) > -1]
        self.instance = None
        if find_apps.__len__()>0:
            self.host = find_apps[0]["host"]
            self.dir  = find_apps[0]["dir"]
            self.app_config = find_apps[0]
            self.app_config["owner"] = self

        self.url = data.url
        self.file = data.file
        self.template = data.template
        pass
    def wrapper(self,*args,**kwargs):
        from . import settings
        self.instance = args[0].__bases__[0].__new__(args[0])
        args[0].__bases__[0].__init__ (self.instance)
        self.instance.__init__()
        if self.host != "":
            def exec_route(*args,**kwargs):
                import pydmobjects
                params_data = kwargs
                if args.__len__()>0:
                    params_data = args[0]

                ret = None
                model = models.model (self,params_data)
                data = models.dmobject ()
                if hasattr (self.app_config["mdl"], "auth"):
                    if request.path != "/" + self.host + "/" + self.app_config["login_url"] and \
                            (not self.app_config["mdl"].auth ()):
                        from flask import redirect
                        return redirect (self.host + "/" + self.app_config["login_url"])
                if request.method == "POST":
                    data = models.dmobject (request.form.to_dict ())
                    call_method = request.headers.get("AJAX-POST",None)
                    if call_method!=None:
                        if hasattr(self.instance,call_method):
                            ret_json = getattr(self.instance,call_method)(request.data)






                from libs.pyfy import settings
                setattr (request, "excutor", self)
                if hasattr(self.instance,"OnLoad"):
                    ret = self.instance.OnLoad(model)
                if request.method == "GET":
                    if hasattr(self.instance,"OnGet"):
                        ret = self.instance.OnGet(model)
                if request.method == "POST":
                    if hasattr(self.instance,"OnPost"):
                        ret = self.instance.OnPost(model)

                if ret == None:
                    html = __render__(
                        "/".join([settings.WORKING_DIR,self.app_config["rel_dir"], "views"]),
                        self.template,model)
                    return html

                else:
                    return ret

            exec_route.func_name = str (self.app_config["rel_dir"].replace ("/", "_")+
                                        "_"+args[0].__module__.replace(".","_")+ "_" +
                                        args[0].__name__)
            self.__flask_app__.add_url_rule (
                "/" + self.host + self.url,
                view_func=exec_route,
                methods=["GET", "POST"]
            )
        else:
            def exec_route(*args,**kwargs):
                model = models.model (self)
                data = models.dmobject ()
                if request.method == "POST":
                    data = models.dmobject (request.form.to_dict ())
                if hasattr (self.app_config["mdl"], "auth"):
                    if not self.app_config["mdl"].auth ():
                        from flask import redirect
                        return redirect ("/" + self.login_url)
                from libs.pyfy import settings
                setattr (request, "excutor", self)
                ret = self.instance.load (model, data)
                model.set_data (data)
                if ret == None:
                    html = __render__(
                        "/".join([settings.WORKING_DIR, self.app_config["rel_dir"], "views"]),
                        self.template,model)
                    return html
                else:
                    return ret

            exec_route.func_name = str (self.app_config["rel_dir"].replace ("/", "_") +
                                        "_" + args[0].__module__.replace (".", "_") + "_" +
                                        args[0].__name__)
            self.__flask_app__.add_url_rule (
                self.url,
                view_func=exec_route,
                methods=["GET", "POST"]
            )




@types(
    url=(str,True),
    template=(str,True)
)
def controller(data):
    import inspect
    file_caller = inspect.stack ()[3][1]
    data.__validator__ = False
    data.file = file_caller

    ret = __controller_wrapper__(data)
    return ret.wrapper

def load():
    from . import settings
    import os
    import sys
    import imp
    import inspect
    from os.path import relpath
    file_name = inspect.stack()[1][1]
    dir_name = os.path.dirname(file_name)
    lst = list(os.walk(dir_name))
    files =[x for x in lst[0][2] if x!="__init__.py" and x[x.__len__()-3:x.__len__()] == ".py"]
    for f in files:
        _f = os.sep.join([dir_name,f])
        rel_p = os.path.relpath(_f, settings.WORKING_DIR)
        mdl_name = rel_p.replace(os.sep, "_").replace(".","__")
        try:
            mdl = imp.load_source(mdl_name,_f)
        except Exception as ex:
            raise Exception("load controller {0} is error".format(_f),ex)


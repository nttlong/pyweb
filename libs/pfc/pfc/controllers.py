from flask import request
from pyparams_validator import types
import models
from flask import render_template
___on_register_view_handler__ = None
__cache_view__ = None
__lst_controllers__ = None
def get_list_of_controllers():
    return __lst_controllers__
class register_controller_model(object):
    def __init__(self):
        self.app_name = None
        self.url = None
        self.template = None
def set_on_register_controller(handler):
    """
    Set handler on register view when system match a new view
    :param handler:
    :return:
    """
    ___on_register_view_handler__ = handler

class Controller(object):
    def __init__(self):
        self.Model = None
        self.ParentController= None
        """The privileges will be dispatch to parent if this property is not empty"""
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
        self.app_name = None
        self.__flask_app__ = settings.app
        find_apps = [x for x in settings.list_of_apps if data.file.find (x["dir"]) > -1]
        self.instance = None
        if find_apps.__len__()>0:
            self.host = find_apps[0]["host"]
            self.dir  = find_apps[0]["dir"]
            self.app_config = find_apps[0]
            self.app_config["owner"] = self
            self.app_name = self.app_config["name"]
        self.url = data.url
        self.file = data.file
        self.template = data.template


    def loadcontroller_info(self,cls_instance):
        global __cache_view__
        global __lst_controllers__
        if __lst_controllers__ == None:
            __lst_controllers__ = []
        if __cache_view__ == None:
            __cache_view__ = {}
        _key_ = "app={0};url={1}".format (self.app_name, self.url).lower ()
        if not __cache_view__.has_key (_key_):
            import threading
            lock = threading.Lock ()
            lock.acquire ()
            try:
                rg = register_controller_model ()
                rg.app_name = self.app_name
                rg.url = self.url
                rg.template = self.template
                rg.methods=[]
                for k,v in cls_instance.__dict__.items():
                    if callable(v) and v.__dict__.has_key("privileges"):
                        rg.methods.append(dict(
                            privileges=v.__dict__["privileges"],
                            description = v.func_doc
                        ))

                if ___on_register_view_handler__ != None:
                    ___on_register_view_handler__ (rg)
                __cache_view__.update ({
                    _key_: rg
                })
                __lst_controllers__.append (rg)
                lock.release ()
            except Exception as ex:
                lock.release ()
                raise ex

    def wrapper(self,*args,**kwargs):
        from . import settings
        self.loadcontroller_info(args[0])
        self.instance = args[0].__bases__[0].__new__(args[0])
        args[0].__bases__[0].__init__ (self.instance)
        self.instance.__init__()
        if self.host != "":
            def exec_route(*args,**kwargs):
                from . import dmobjs
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
                if request.method == "GET":

                    if hasattr(self.instance,"Model") and self.instance.Model != None:
                        from pymqr import documents
                        if not isinstance(self.instance.Model,documents.BaseDocuments):
                            raise Exception("Model of controller {0} must be sub class of {1}".format(
                                type(self.instance),documents.BaseDocuments
                            ))
                        model.defaultData = (self.instance.Model<<{}).to_dict()

                if request.method == "POST":
                    data = models.dmobject (request.form.to_dict ())
                    call_method = request.headers.get("AJAX-POST",None)
                    if call_method!=None:
                        if hasattr(self.instance,call_method):
                            from . import dmobjs
                            from . import JSON
                            from flask import Response
                            model = models.model (self,JSON.from_json(request.data))
                            # data = dmobjs.pdmobject(JSON.from_json(request.data))
                            ret_data = getattr(self.instance,call_method)(model)
                            ret_json=JSON.to_json(ret_data)
                            return ret_json, 200, {'Content-Type': 'application/json; charset=utf-8'}

                from . import settings
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
                from . import settings
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
            import importlib
            sys.path.append (os.path.dirname (_f))
            mdl = imp.load_source(mdl_name,_f)
        except Exception as ex:
            raise Exception("load controller {0} is error".format(_f),ex)


class __privileges_wrapper__():
    def __init__(self,name):
        self.name = name
    def wrapper(self,*args,**kwargs):
        if not args[0].__dict__.has_key("privileges"):
            args[0].__dict__.update({
                "privileges":{}
            })
        args[0].__dict__["privileges"].update({
            self.name:True
        })
        return args[0]

def __resolve_mapper__(name,*args,**kwargs):
    ret= __privileges_wrapper__(name)
    return ret.wrapper
class privileges():

    @staticmethod
    def View():
        return __resolve_mapper__("view")
    @staticmethod
    def Insert(*args,**kwargs):
        return __resolve_mapper__ ("insert" )
    @staticmethod
    def Update():
        return __resolve_mapper__ ("update")
    @staticmethod
    def Delete():
        return __resolve_mapper__ ("delete")
    @staticmethod
    def Delete():
        return __resolve_mapper__ ("view")
    @staticmethod
    def Publish():
        return __resolve_mapper__ ("publish")
    @staticmethod
    def Print():
        return __resolve_mapper__ ("print")
    @staticmethod
    def Export():
        return __resolve_mapper__ ("export")

    @staticmethod
    def Import():
        return __resolve_mapper__ ("import", )
    @staticmethod
    def Custom(privilege):
        return __resolve_mapper__ (privilege, )


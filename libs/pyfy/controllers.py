from flask import request
from pyparams_validator import types
import models
from flask import render_template

class Controller(object):
    @property
    def request(self):
        from flask import request
        return request

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

            def exec_route():

                model = models.model (self)
                data = models.dmobject ()
                if request.method == "POST":
                    data = models.dmobject (request.form.to_dict ())

                if hasattr (self.app_config["mdl"], "auth"):
                    if request.path != "/" + self.host + "/" + self.app_config["login_url"] and \
                            (not self.app_config["mdl"].auth ()):
                        from flask import redirect
                        return redirect (self.host + "/" + self.app_config["login_url"])

                from libs.pyfy import settings
                setattr (request, "excutor", self)

                ret = self.instance.load(model, data)

                model.set_data (data)
                if ret == None:
                    return render_template ("/".join ([self.app_config["rel_dir"], "views", self.template]),
                                            **model.__dict__)

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

            def exec_route():
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
                    return render_template ("/".join ([self.app_config["rel_dir"], "views", self.template]), **model)
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
    template=(str,True))
def controller(data):
    import inspect
    file_caller = inspect.stack ()[3][1]
    data.__validator__ = False
    data.file = file_caller

    ret = __controller_wrapper__(data)
    return ret.wrapper



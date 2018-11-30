
VERSION = [0,0,0,"beta",0]
def get_version():
    return VERSION[0].__str__()+\
           "."+VERSION[1].__str__()+\
           "."+VERSION[2].__str__()+\
           "."+VERSION[3].__str__()+\
           "."+VERSION[4].__str__()
__urlpatterns__ = None

__working_dir__ = None
def set_working_dir(_dir):
    global __working_dir__
    __working_dir__ = _dir


from django.conf.urls import include, url
from django.http import HttpResponse


def set_urlpatterns(urlpatterns):
    __urlpatterns__ = urlpatterns

class Controller(object):
    def __init__(self):
        pass
def __get_server_static__(app_path,static_dir):
    """
    get full server static path where static file store at server
    :return:
    """
    import os
    # from . import config_loader

    # root_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    _path = (static_dir).replace("/", os.path.sep)
    return os.sep.join([app_path, _path])
def __get_static_url__(app_name,host_dir,app_path,static_dir):
    if host_dir == "":
        return url(r'^' + app_name + '/static/(?P<path>.*)$', 'django.views.static.serve',
                   {'document_root': __get_server_static__(app_path,static_dir), 'show_indexes': True})
    else:
        return url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
                   {'document_root': __get_server_static__(app_path,static_dir), 'show_indexes': True})
def __render__(template_dir,fileName,data,request):
    import os
    from mako.lookup import TemplateLookup
    from  mako import lookup
    from mako import exceptions
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
    return HttpResponse(outputText)


class __controller_wrapper__(object):
    def __init__(self,*args,**kwargs):
        import sys,regex
        data = args[0]
        self.app_rel_dir = data['app_rel_dir']
        self.__has_init_static__ = False
        self.url = data["controller_url"]
        self.app_path = data["app_path"]
        self.app_dir =data["app_dir"]
        self.app_module_name = data["app_module_name"]

        self.template = data["controller_template"]
        self.controller_type = None
        self.controller_instance = None
        self.mdl = sys.modules[self.app_module_name]
        if not hasattr(self.mdl,"NAME"):
            raise Exception("'{0}' was not found in '{1}'".format("NAME",self.mdl))
        self.app_name = self.mdl.NAME
        if not hasattr(self.mdl,"STATIC"):
            raise Exception("'{0}' was not found in '{1}'".format("STATIC",self.mdl))
        self.static = self.mdl.STATIC
        if not hasattr(self.mdl,"HOST_DIR"):
            raise Exception("'{0}' was not found in '{1}'".format("HOST_DIR",self.mdl))

        self.host_dir = self.mdl.HOST_DIR
        if not hasattr(self.mdl,"DB_PREFIX"):
            raise Exception("'{0}' was not found in '{1}'".format("DB_PREFIX", self.mdl))
        self.db_prefix = self.mdl.DB_PREFIX
        if not hasattr(self.mdl,"USE_URL_PREFIX"):
            raise Exception("'{0}' was not found in '{1}'".format("USE_URL_PREFIX", self.mdl))
        if not isinstance(self.mdl.USE_URL_PREFIX,bool):
            raise Exception("'{0}' was must be  '{1}'".format("USE_URL_PREFIX", bool))
        self.use_url_prefix = self.mdl.USE_URL_PREFIX
        from pathlib import Path
        self.working_dir = Path(self.app_dir).parent.parent.__str__()
    def exec_url(self,request,*args,**kwargs):
        from . import models
        from . import dmobj

        data_params = kwargs
        if args.__len__() > 0:
            data_params = args[0]
        model =  models.Model(data_params,request, self)
        model.request = request

        model.params = dmobj.lazyobject(data_params)
        model.user = request.user
        if (model.appUrl+"/"+self.mdl.LOGIN_URL).lower()!=(model.absUrl+request.path).lower():
            if hasattr(self.mdl,"auth"):
                if not self.mdl.auth(model):
                    from django.shortcuts import redirect
                    return redirect(model.appUrl+"/"+self.mdl.LOGIN_URL)
        if request.method == "GET":
            if hasattr(self.controller_instance,"OnGet"):
                ret = self.controller_instance.OnGet(model)
                if ret != None:
                    return ret
                else:
                    return __render__(self.app_dir+"/views",self.template,model,request)
            else:
                return __render__(self.app_dir + "/views", self.template, model, request)





    def wrapper(self,*args,**kwargs):
        import sys,re
        self.controller_type = args[0]
        # if not hasattr(args[0],"__init__"):
        #     raise Exception("'__init__' of {0} was not found")
        # import inspect
        # params = inspect.getargspec(args[0].__init__)

        self.controller_instance = self.controller_type.__bases__[0].__new__(self.controller_type)
        super(self.controller_type, self.controller_instance).__init__()
        if hasattr(self.controller_instance,"__init__"):
            self.controller_instance.__init__()
        if __urlpatterns__ == None:
            static_url = __get_static_url__(self.app_name,self.host_dir,self.app_dir,self.static)
            if not sys.modules.has_key("{0}.urls".format(self.app_module_name)):
                import imp
                mdl = imp.new_module("{0}.urls".format(self.app_module_name))
                setattr(mdl,"urlpatterns",[static_url])
                sys.modules.update({
                    "{0}.urls".format(self.app_module_name):mdl
                })
            else:
                mdl = sys.modules[self.app_module_name+".urls"]
            urlpatterns = getattr(mdl,"urlpatterns")
            urlpatterns.append(url(re.compile("^"+self.url+"$").pattern , self.exec_url))

        else:
            if not self.__has_init_static__:
                __urlpatterns__.append(__get_static_url__(self.app_name,self.host_dir,self.app_dir,self.static))
                self.__has_init_static__ = True

            if self.use_url_prefix:
                # //?P<path>.*)
                if self.host_dir != "":
                    __urlpatterns__.append(url(re.compile("^(?P<tenancy_code>\w+)/"+self.host_dir+"/" + self.url + "$").pattern, self.exec_url))
                else:
                    __urlpatterns__.append(url(re.compile("^(?P<tenancy_code>\w+)/" + self.url + "$").pattern, self.exec_url))
            else:
                if self.host_dir != "":
                    __urlpatterns__.append(url(re.compile("^"+self.host_dir +"/"+ self.url + "$").pattern, self.exec_url))
                else:
                    __urlpatterns__.append(url(re.compile("^"+self.url+"$").pattern , self.exec_url))

        pass

def controller(*args,**kwargs):
    """
    Example controller(url='/index',template='index.html')
    :param args:
    :param kwargs:
    :return:
    """
    global __working_dir__
    if __working_dir__ == None:
        raise Exception("It looks like you forgot call djcontroller.set_working_dir")
    import inspect,sys,os
    from os.path import relpath

    app_path = inspect.stack()[2][1]
    app_dir = os.path.dirname(app_path)
    app_rel_dir = relpath(app_dir,__working_dir__)
    app_module_name = app_dir.split(os.sep)[app_dir.split(os.sep).__len__()-1]
    controller_url = kwargs["url"]
    controller_template = kwargs["template"]


    wr =__controller_wrapper__(dict(
        app_path=app_path,
        app_dir =app_dir,
        app_module_name= app_module_name,
        controller_url =controller_url,
        controller_template =controller_template,
        app_rel_dir=app_rel_dir
    ))
    return wr.wrapper



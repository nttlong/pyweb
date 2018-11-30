from . import dmobj
__cache_res__ = None
import threading
lock = threading.Lock()
class ResCaption(object):
    def __getattr__(self, item):
        return item
class ModelRes(object):
    def __init__(self,owner):
        self.owner = owner
    def __gt__(self, other):
        return self.owner.appRes(other)
    def __rshift__(self, other):
        return other
    def __floordiv__(self, other):
        return other


class Model(object):
    def __init__(self,data_params,request,owner):
        self.user = None
        self.static_path = None
        self.request = None
        if owner.use_url_prefix:
            self.db_prefix = owner.db_prefix
        else:
            self.db_prefix = data_params["tenancy_code"]

        self.params = dmobj.lazyobject(data_params)
        self.language = request.session.get("language","en")
        self.view_id = owner.template
        self.viewId = owner.template


        request.get_host()
        def __get_abs_url__():
            n = request.path.lstrip("/").rstrip("/").split("/").__len__()
            return request.build_absolute_uri("."*n).rstrip("/")
        def __get_app_url__():
            if hasattr(self.params,""):
                return (__get_abs_url__()+"/"+self.params.tenancy_code+"/"+owner.host_dir).rstrip("/")
            else:
                return (__get_abs_url__() + "/"+owner.host_dir).rstrip("/")
        def __get_static__():
            return  __get_abs_url__()+"/"+owner.host_dir+"/static"
        def __get_res_item__(language,app,view,key,value=None):
            language = language.lower()
            app = app.lower()
            view = view.lower()
            if value == None:
                value = key.lstrip(" ").rstrip(" ")
                key = value.lower()

            global  __cache_res__
            if __cache_res__ == None:
                __cache_res__ ={}
            if not hasattr(owner.mdl,"GetResItem"):
                raise Exception("'{0} is not declare in '{1}".format("GetResItem",owner.mdl))
            k = "schema={0};lan={1};app={2};view={3};key={4}".format(self.db_prefix, language,self.view_id,app,key,value)
            if not __cache_res__.has_key(k):
                lock.acquire()
                try:
                    ret = owner.mdl.GetResItem(self.db_prefix, language,app,view,key,value)
                    __cache_res__.update({
                        k:ret
                    })
                    lock.release()
                    return ret
                except Exception as ex:
                    lock.release()
                    raise ex
            else:
                return __cache_res__[k]

        def __get_global_res__(key,value = None):
            return __get_res_item__(self.language,"-","-",key,value)
        def __get_app_res__(key,value = None):
            return __get_res_item__(self.language,owner.app_name,"-",key,value)
        def __get_res__(key,value = None):
            return __get_res_item__(self.language,owner.app_name,"-",key,value)




        self.static = __get_static__()
        self.absUrl=__get_abs_url__()
        self.get_abs_url = __get_abs_url__
        self.appUrl = __get_app_url__()
        self.get_app_url =  __get_app_url__
        self.get_global_res = __get_global_res__
        self.gRes = __get_global_res__
        self.get_app_res = __get_app_res__
        self.appRes = __get_app_res__
        self.appDirViews = owner.app_rel_dir+"/views"
        self._ = ModelRes(self)







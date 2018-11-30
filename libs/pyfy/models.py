from flask import request,session
from os.path import relpath
import os
import pymqr
from pymqr import documents
__has_languages__ = None
from threading import Lock
from . import settings
import pydmobjects
lock = Lock()

@documents.Collection("languages")
class Languages(object):
    def __init__(self):
        self.app = str,True
        self.language = str,True
        self.key = str,True
        self.view = str,True

class model(object):
    def __init__(self,excutor,param_data):
        self.excutor = excutor
        self.absUrl = request.url.split("://")[0]+"://"+request.host
        self.appUrl = self.absUrl+"/"+self.excutor.host
        self.static = self.absUrl + "/" + self.excutor.host+"/static"
        self.appName =self.excutor.app_config["app_name"]
        self.language = session.get("language","en")
        self.appDir = relpath(self.excutor.dir,settings.WORKING_DIR).replace(os.sep,"/")
        self.appDirViews = self.appDir+"/views"
        self.params = dmobject(param_data)
        self.currentUrl=self.absUrl+request.path
        self.data = dmobject({})


    def getAppRes(self,key,value = None):
        if value == None:
            value = key.lstrip(" ").rstrip(" ")
        key = key.lstrip (" ").rstrip (" ").lower()

        global __has_languages__
        if __has_languages__ == None:
            __has_languages__ = {}
        find_key = "lang={0};app={1};key={2}".format(self.language, self.appName,key)
        ret= __has_languages__.get(find_key,None)
        if ret!=None:
            return ret
        else:
            import pymqr.settings as st
            qr = pymqr.query(st.getdb(),Languages)
            lock.acquire()
            try:
                ret_obj= qr.where(pymqr.funcs.expr((Languages.language== self.language) &
                                                   (Languages.key == key) &
                                                   (Languages.app == self.appName))).object
                if ret_obj.is_empty():
                    ret_obj = Languages<<{
                        Languages.language:self.language,
                        Languages.app:self.appName,
                        Languages.key:key
                    }
                    ret,error,result = qr.insert(ret_obj.to_dict()).commit()
                    if error != None:
                        raise error
                    __has_languages__.update({
                        find_key:value
                    })
                lock.release()
                return value
            except Exception as ex:
                lock.release()
                raise ex


# encoding=utf8
VERSION = [1,0,0,"final",0]
def get_version():
    return VERSION[0].__str__()+\
           "."+VERSION[1].__str__()+\
           "."+VERSION[2].__str__()+\
           "."+VERSION[3].__str__()+\
           "."+VERSION[4].__str__()
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import datetime
class __validator_class__(object):
    def __init__(self):
        # self.__properties__ ={}
        self.__data_type__ = None
        self.__require__ = False
        self.__dict__.update({"__properties__":{}})
        self.__dict__.update({"__validator__": False})

        # self.__validator__= False
    def __getattr__(self, item):
        if self.__dict__.get("__validator__",False):
            if not self.__dict__.get("__properties__",{}).has_key(item):
                raise (Exception("'{0}' was not found".format(item)))
        return super(__validator_class__, self).__getattr__(item)
    def __setattr__(self, key, value):
        if key[0:2] == "__":
            super(__validator_class__, self).__setattr__(key, value)
            return
        if value == None:
            super(__validator_class__, self).__setattr__(key, value)
            return
        __data_type__ = self.__dict__.get("__properties__",{}).get('type',None)
        if __data_type__ == "object" and not type(value) is dmobject:
            raise Exception("'{0}' is invalid data type, expected type is {1}, but the value is {2}".format(key,__data_type__,value))
        if __data_type__ == "text" and not type(value) in [str,unicode]:
            raise Exception(
                "'{0}' is invalid data type, expected type is {1}, but the value is {2}".format(key, self.__data_type__,
                                                                                                value))
        if __data_type__ == "date" and not type(value) is datetime.datetime:
            raise Exception(
                "'{0}' is invalid data type, expected type is {1}, but the value is {2}".format(key, self.__data_type__,
                                                                                                value))
        if __data_type__ == "bool" and not type(value) is bool:
            raise Exception(
                "'{0}' is invalid data type, expected type is {1}, but the value is {2}".format(key, self.__data_type__,
                                                                                                value))



        super(__validator_class__, self).__setattr__(key, value)
    def __set_config__(self,property,type,require):
        self.__properties__.update({
            property:dict(
                type=type,
                require=require
            )
        })
class dmobject(__validator_class__):
    def __init__(self,*args,**kwargs):

        data = kwargs
        if args.__len__()>0:
            data = args[0]
        if data == None:
            self = None
            return
        if data != {}:
            self.__dict__.update({"__validator__": False})
            for k,v in data.items():
                if k[0:2] != "__" and k.count('.') == 0:
                    self.__properties__.update({k:1})
                    if type(v) is dict:
                        setattr(self,k,dmobject(v))
                    elif type(v) is list:
                        values = []
                        for x in v:
                            if type(x) is dict:
                                values.append(dmobject(x))
                            else:
                                values.append(x)
                        setattr(self,k,values)
                    else:
                        setattr(self, k, v)
            self.__dict__.update({"__validator__": True})
    def __to_dict__(self):
        keys = [x for x in self.__dict__.keys() if x[0:2] != "__"]
        if keys == []:
            return None
        ret = {}
        for k in keys:
            v= self.__dict__[k]
            if hasattr(v,"__to_dict__"):
                ret.update({k:v.__to_dict__()})
            elif type(v) is list:
                lst = []
                for x in v:
                    if hasattr(x,"__to_dict__"):
                        lst.append(x.__to_dict__())
                    else:
                        lst.append(x)
                ret.update({k: lst})
            else:
                ret.update({k:v})
        return ret
    def __getattr__(self, item):
        if item =="__properties__":
            if self.__dict__.has_key(item):
                return self.__dict__[item]
            else:
                self.__dict__.update({item:{}})
                return self.__dict__[item]

        return super(dmobject, self).__getattr__(item)
    def __setattr__(self, key, value):
        super(dmobject, self).__setattr__(key, value)
    def __is_emty__(self):
        return self.__dict__ == {}


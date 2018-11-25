db = None
app = None
list_of_apps =None
APP_NAME = None
WORKING_DIR = None
from flask import Flask
from pymongo import database
import pymongo
from ..MongodDbSession import MongoSessionInterface
import os
from pyparams_validator import types
@types(
    NAME=(str,True),
    DB = (dict(
        HOST=(str,True),
        PORT = (int,True),
        NAME = (str,True),
        USER = (str,True),
        PASSWORD = (str,True)
    ),True),
    WORKING_DIR =(str,True),
    CONFIG=(dict(
        SECRET_KEY = (str,True),
        SESSION_COOKIE_NAME = (str,True)
    ),True),
    APPS=([dict(
        NAME=(str,True),
        DIR = (str,True),
        HOST_DIR =(str,True),
        LOGIN_URL = (str,True)
    )],True)
)

def init(data):
    global db
    global list_of_apps
    global app
    global WORKING_DIR
    global APP_NAME
    if list_of_apps == None:
        list_of_apps = []
    APP_NAME =data.NAME
    WORKING_DIR = data.WORKING_DIR

    cnn = pymongo.MongoClient (
        host=data.DB.HOST,
        port=data.DB.PORT
    )
    db = cnn.get_database (data.DB.NAME)
    db.authenticate (data.DB.USER,data.DB.PASSWORD)
    app = Flask (data.NAME,template_folder = data.WORKING_DIR)
    jinja_options = app.jinja_options.copy ()
    jinja_options.update (dict (
        variable_start_string='{(',
        variable_end_string=')}'
    ))
    app.session_interface = MongoSessionInterface (db=db)
    app.secret_key = "57thvy5^%"
    #template_folder
    for app_info in data.APPS:
        import sys

        paths = app_info.DIR.split("/")
        dir = os.sep.join([x for x in paths if paths.index(x)<paths.__len__()-1])
        _path = os.sep.join([data.WORKING_DIR,dir])
        sys.path.append (_path)
        app_config_item = dict(
            dir = os.sep.join([_path,app_info.DIR.split("/")[app_info.DIR.split("/").__len__()-1]]),
            host = app_info.HOST_DIR,
            rel_dir = app_info.DIR,
            login_url = app_info.LOGIN_URL
        )
        list_of_apps.append(app_config_item)
        mdl_name = app_info.DIR.split("/")[app_info.DIR.split("/").__len__()-1]
        mdl = __import__(mdl_name)
        app_config_item["mdl"] = mdl
        app_config_item["app_name"] = app_info.NAME
        app_config_item["owner"].name = app_info.NAME
        app_config_item["owner"].login_url = app_info.LOGIN_URL
        app_config_item["owner"].rel_dir = app_info.DIR

        def static_proxy(path):
            from flask import send_from_directory
            x=app_info
            _path = os.sep.join([data.WORKING_DIR,app_info.DIR+"/static/"]).replace("/",os.sep)
            return send_from_directory (_path,path)

            static_proxy.func_name = app_info.DIR.replace ("/", "_") + "_static_serve"
        app.add_url_rule (
            "/"+app_info.HOST_DIR+'/static/<path:path>',
            view_func=static_proxy,
            methods=["GET"]
        )










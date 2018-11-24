import pymongo
import pymqr
from flask import Flask
from flask_session import Session
import os
import apps

from pymqr import settings
cnn = pymongo.MongoClient(
    host = "localhost",
    port =27017
)
db = cnn.get_database("db1")
db.authenticate("root","123456")
settings.setdb(db)
APP_NAME = "__main__"
WORKING_DIR = os.getcwd()
TEMPLATE_PATH =os.sep.join([WORKING_DIR,"views"])
app = Flask(APP_NAME,template_folder=TEMPLATE_PATH)
app.config.update(
    SECRET_KEY=b'_5#y2L"F4Q8z\n\xec]/',
    SESSION_COOKIE_NAME ="main"
)
jinja_options = app.jinja_options.copy()
jinja_options.update(dict(
    variable_start_string='{(',
    variable_end_string=')}'
))
app.jinja_options=jinja_options
# app.config['SECRET_KEY'] = 'hf437$#7y'
app.secret_key="57thvy5^%"
# Session(app)
app.session_interface =apps.MongodDbSession.MongoSessionInterface(db=db)
app.secret_key="57thvy5^%"

from libs.pyfy import routes
from flask import request,session
@routes.route(
    url="/",
    file = __file__,
    template="index.html")
def index():
    session["X"]=1
    x=1
    pass
@routes.route(
    url="/login",
    file = __file__,
    template = "login.html"
)
def login():
    return {}
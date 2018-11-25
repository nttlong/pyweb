from libs.pyfy import routes
from flask import request
@routes.route(
    url="/",
    file = __file__,
    template="index.html")
def index(*args,**kwargs):
    x=1
    pass
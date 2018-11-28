from libs.pyfy import controllers
import pymqr.mobject
from flask import session
@controllers.controller(
    url="/login",
    template = "login.html"
)
class Login(controllers.Controller):
    def load(self):
        pass
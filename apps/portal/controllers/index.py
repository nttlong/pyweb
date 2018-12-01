from pfc import controllers
import pymqr.mobject
from flask import session
@controllers.controller(
    url="/",
    template="index.html"
)
class index(controllers.Controller):
    def OnGet(self,sender,model):
        pass
from libs.pyfy import controllers
import pymqr.mobject
from flask import session
@controllers.controller(
    url="/",
    template="index.html"
)
class index(controllers.Controller):
    def OnGet(self,sender,model):
        x=self.request
        dmobj = pymqr.mobject.dynamic_object
        sender.user = pymqr.mobject.dynamic_object (session["user"])
        sender.menu = [
            dmobj (
                caption="System",
                items=[
                    dmobj (
                        caption="Users",
                        page="views/users"
                    )
                ]
            ),
            dmobj (
                caption="Resource",
                items=[
                    dmobj (
                        caption="Languages",
                        page="views/language"
                    )
                ]
            )
        ]
        # super(index,self).__init__()






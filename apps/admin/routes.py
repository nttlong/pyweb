from libs.pyfy import routes
from flask import request,session,redirect
from libs import memberships
@routes.route(
    url="/",
    template="index.html")
def index(sender,model):
    session["X"]=1
    x=1
    pass
@routes.route(
    url="/login",
    template = "login.html"
)
def login(sender,model):

    if request.method== "POST":
        ret= memberships.validate_user(request.form.to_dict())
        if ret!=None:
            memberships.SignIn(
                Session=session,
                User=ret,
                Language=sender.language)
            return redirect(sender.appUrl)
        else:
            model.error=sender.get_app_res("Login fail!!!")

        data =request.data

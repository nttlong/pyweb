from pyparams_validator import types
@types(
    UserName = (str,True), #Username is require
    Password = (str,True), #Password is require
    Email = (str,True), #Email is requie
)
def create_user(data):

    pass
import routes
from libs import memberships
from  libs.memberships import users
from flask import session
import pymqr

from . import controllers
def auth():

    user = memberships.find_user(pymqr.filters.UserName=="system")
    if user.is_empty():
        memberships.create_user(
            UserName="system",
            Password="system",
            Email="",
            IsSysAdmin=True,
            IsActive = True
        )

    user = session.get("user",{})
    if user== {}:
        return False
    else:
        return user.get("IsSysAdmin",False)





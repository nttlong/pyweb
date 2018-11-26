# import settings
from flask import Flask
from flask_session import Session
import os
from libs.pyfy import settings

settings.init(
    CONFIG=dict(
        SECRET_KEY="1ewqne",
        SESSION_COOKIE_NAME = "main"

    ),
    WORKING_DIR = os.getcwd(),
    DB = dict(
        HOST = "localhost",
        PASSWORD ="123456",
        NAME ="db1",
        PORT =27017,
        USER ="root"
    ),
    NAME ="main",
    APPS =[
        dict(
            NAME = "admin",
            DIR = "apps/admin",
            HOST_DIR = "admin",
            LOGIN_URL ="login"

        )
    ]

)
from pymqr import settings as st
st.setdb(settings.db)
# import routes
if __name__ == "__main__":

    settings.app.run(debug=True)
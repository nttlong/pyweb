from flask import Flask
from flask import session
from flask import render_template
import settings
app = settings.app
@app.route("/")
def home():
    session["x"]=12345
    import flask_session
    flask_session.sessions
    return render_template("index.html",name = "123456")
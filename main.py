import settings
from flask import Flask
from flask_session import Session

import routes
if __name__ == "__main__":

    settings.app.run(debug=True)
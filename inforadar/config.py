from flask import Flask
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

import inforadar.db_data as db_data

app = Flask(__name__)
# Configure the SqlAlchemy part of the app instance
app.config["SQLALCHEMY_ECHO"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = db_data.postgres_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["REMEMBER_COOKIE_HTTPONLY"] = True

try:
    app.config.from_envvar("GOOGLE_CONFIG_PATH")
except RuntimeError:
    pass

# Create the SqlAlchemy db instance
db = SQLAlchemy(app)

# Initialize Marshmallow
ma = Marshmallow(app)

# Initialize Login
login = LoginManager()
login.init_app(app)
login.session_protection = 'strong'

app.secret_key = app.config['SECRET_KEY']

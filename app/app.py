from flask import Flask, g, request, session
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from config import Configuration
from flask_login import LoginManager, current_user
from flask_bcrypt import Bcrypt
import os

app = Flask(__name__)

APPLICATION_DIR = os.path.dirname(os.path.realpath(__file__))
app.config['SECRET_KEY'] = 'secret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s/nsp.db' % APPLICATION_DIR
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"

bcrypt = Bcrypt(app)

@app.before_request
def _before_request():
    g.user = current_user


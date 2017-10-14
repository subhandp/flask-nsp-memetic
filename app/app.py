from flask import Flask, g, request, session
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from config import Configuration
import os
#import views

app = Flask(__name__)

APPLICATION_DIR = os.path.dirname(os.path.realpath(__file__))
app.config['SECRET_KEY'] = 'secret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s/nsp.db' % APPLICATION_DIR
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# app.config.from_object(Configuration) # use value from our Config

db = SQLAlchemy(app)
#
# migrate = Migrate(app, db)
# manager = Manager(app)
# manager.add_command('db', MigrateCommand)

from flask import Flask, g, request, session
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from config import Configuration
#import views

app = Flask(__name__)
app.config.from_object(Configuration) # use value from our Config
db = SQLAlchemy(app)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os

UPLOAD_FOLDER = '/static/Profile_Icon'
ALLOWED_EXTENSIONS = set(['png', 'jpg'])

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://cwnujwrehpjyzd:8abe83e2c3989fe882695498ae4f2dfe19196347f12886e550bceec8e29c3aa0@ec2-63-34-180-86.eu-west-1.compute.amazonaws.com:5432/det4qasac9ptet'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '592dc58d1229ead98e47754f4d744767'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
from manflix import routes
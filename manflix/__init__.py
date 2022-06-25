from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://bdldqggxugdpmk:1f49563c3fef3d73da737a2d808ef2077b314fc2d7e96c96f4a4cfbbd0ceb5f6@ec2-63-32-248-14.eu-west-1.compute.amazonaws.com:5432/dd2j322ej2nn9s'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '592dc58d1229ead98e47754f4d744767'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from manflix import routes
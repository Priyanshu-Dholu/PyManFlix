from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

# For Offline
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'

# For Heroku DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://tagqsilmewdzer:bf7cf5abc49f1c48d9bf92f7a70fab51662863b1fa4a74961e47b05460ebe246@ec2-52-214-23-110.eu-west-1.compute.amazonaws.com:5432/ddm4jsmvs45cdf'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '592dc58d1229ead98e47754f4d744767'
db = SQLAlchemy(app)

from manflix import routes
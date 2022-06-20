from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://wyhhpedpahpaka:5d5898e5c8eac66bb381de043cf7e1c33a71c568842cbba0aa8db5ccebb4526a@ec2-176-34-215-248.eu-west-1.compute.amazonaws.com:5432/debanb9vaqfgp0'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '592dc58d1229ead98e47754f4d744767'
db = SQLAlchemy(app)

from manflix import routes
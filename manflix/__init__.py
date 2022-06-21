from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://bdldqggxugdpmk:1f49563c3fef3d73da737a2d808ef2077b314fc2d7e96c96f4a4cfbbd0ceb5f6@ec2-63-32-248-14.eu-west-1.compute.amazonaws.com:5432/dd2j322ej2nn9s'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '592dc58d1229ead98e47754f4d744767'
db = SQLAlchemy(app)

from manflix import routes
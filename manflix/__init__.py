from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://kmveufrmdneasy:2e7e356e38b73737adb9c0eaee5a0dbb412ce89a58d10dc676f60026a9ea76ec@ec2-3-224-8-189.compute-1.amazonaws.com:5432/d5jo1q9gqqa32h'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '592dc58d1229ead98e47754f4d744767'
db = SQLAlchemy(app)

from manflix import routes
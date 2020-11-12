import datetime
from enum import Enum
from server import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    oauth_id = db.Column(db.String(255))
    name = db.Column(db.String(255))
    username = db.Column(db.String(255))
    email = db.Column(db.String(320), unique=True)
    registration_datetime = db.Column(db.DateTime, default=datetime.datetime.utcnow())


class LoginType(Enum):
    GOOGLE = "google"
    PASSWORD = "password"

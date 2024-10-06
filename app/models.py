from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base


db = SQLAlchemy(model_class=automap_base())


class User(db.Model):
    __tablename__ = "users"


class Therapist(db.Model):
    __tablename__ = "therapists"


class Role(db.Model):
    __tablename__ = "roles"


class Review(db.Model):
    __tablename__ = "reviews"


class Appointment(db.Model):
    __tablename__ = "appointments"


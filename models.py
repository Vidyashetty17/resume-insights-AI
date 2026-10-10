from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):

    __tablename__ = "users"
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(60),nullable = False)
    email = db.Column(db.String(30),nullable = False ,unique = True)
    password_hash = db.Column(db.String(50),nullable = False )
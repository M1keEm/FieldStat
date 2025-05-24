from backendFlask import db

class User(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    username = db.Column("username", db.String(80), unique=True, nullable=False)
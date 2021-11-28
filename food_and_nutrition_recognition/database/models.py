from database.db import db_obj


class User(db_obj.Model):
    id = db_obj.Column(db_obj.Integer, primary_key=True)
    public_id = db_obj.Column(db_obj.String(50), unique=True)
    name = db_obj.Column(db_obj.String(50))
    password = db_obj.Column(db_obj.String(80))


class Img(db_obj.Model):
    id = db_obj.Column(db_obj.Integer, primary_key=True)
    img = db_obj.Column(db_obj.Text, unique=True, nullable=False)
    name = db_obj.Column(db_obj.Text, nullable=False)
    mimetype = db_obj.Column(db_obj.Text, nullable=False)

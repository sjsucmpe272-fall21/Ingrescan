from database.db import db_obj


class user_data(db_obj.Model):
    public_u_id = db_obj.Column(db_obj.String(50), primary_key=True)
    u_fname = db_obj.Column(db_obj.String(100))
    u_lname = db_obj.Column(db_obj.String(100))
    u_phone = db_obj.Column(db_obj.String(20))
    u_email = db_obj.Column(db_obj.String(100))
    u_pwd = db_obj.Column(db_obj.String(50))    


class user_food_data(db_obj.Model):
    f_id = db_obj.Column(db_obj.Integer, primary_key=True)
    public_u_id = db_obj.Column(db_obj.String(50))
    image = db_obj.Column(db_obj.Text, unique=True, nullable=False)
    foodname = db_obj.Column(db_obj.String(50), nullable=False)
    mimetype = db_obj.Column(db_obj.String(50), nullable=False)

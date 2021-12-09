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
    public_u_id = db_obj.Column(db_obj.String(50), nullable=False)
    image = db_obj.Column(db_obj.Text, unique=True, nullable=False)
    foodname = db_obj.Column(db_obj.String(100), nullable=False)
    mimetype = db_obj.Column(db_obj.String(20), nullable=True)
    timestamp = db_obj.Column(db_obj.String(20), nullable=False)


class user_nutrition_history(db_obj.Model):
    n_id = db_obj.Column(db_obj.Integer,  primary_key=True)
    f_id = db_obj.Column(db_obj.Integer, nullable=False)
    public_u_id = db_obj.Column(db_obj.String(50), nullable=False)
    energy_100g = db_obj.Column(db_obj.Float, nullable=False)
    carbohydrates_100g = db_obj.Column(db_obj.Float, nullable=False)
    sugars_100g = db_obj.Column(db_obj.Float, nullable=False)
    proteins_100g = db_obj.Column(db_obj.Float, nullable=False)
    fat_100g = db_obj.Column(db_obj.Float, nullable=False)
    fiber_100g = db_obj.Column(db_obj.Float, nullable=False)
    cholesterol_100g = db_obj.Column(db_obj.Float, nullable=False)
    timestamp = db_obj.Column(db_obj.String(20), nullable=False)

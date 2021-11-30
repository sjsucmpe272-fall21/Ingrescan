from app import db_obj


class user_data(db_obj.Model):
    # id = db_obj.Column(db_obj.Integer, primary_key=True)
    # public_id = db_obj.Column(db_obj.String(50), unique=True)
    # name = db_obj.Column(db_obj.Strqing(50))
    # password = db_obj.Column(db_obj.String(80))
    # u_id = db_obj.Column(db_obj.Integer, primary_key=True)
    public_u_id = db_obj.Column(db_obj.String(50), primary_key=True)
    u_fname = db_obj.Column(db_obj.String(100))
    u_lname = db_obj.Column(db_obj.String(100))
    u_phone = db_obj.Column(db_obj.String(20))
    u_email = db_obj.Column(db_obj.String(100))
    u_pwd = db_obj.Column(db_obj.String(50))    


class user_food_data(db_obj.Model):
    # id = db_obj.Column(db_obj.Integer, primary_key=True)
    # img = db_obj.Column(db_obj.Text, unique=True, nullable=False)
    # name = db_obj.Column(db_obj.Text, nullable=False)
    # mimetype = db_obj.Column(db_obj.Text, nullable=False)
    # userId = db_obj.Column(db_obj.String(50))
    f_id = db_obj.Column(db_obj.Integer, primary_key=True)
    public_u_id = db_obj.Column(db_obj.String(50))
    image = db_obj.Column(db_obj.Text, unique=True, nullable=False)
    foodname = db_obj.Column(db_obj.String(50), nullable=False)
    mimetype = db_obj.Column(db_obj.String(50), nullable=False)

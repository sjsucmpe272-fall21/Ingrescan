from fastai.vision.image import open_image
from flask import Flask, request, jsonify, make_response
from fastai.vision import *
import pandas as pd
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import uuid
from database.models import *
from scripts.utils import api_config_init, food_predict, get_nutrition_info, recommend_food
import os
from flask_sqlalchemy import SQLAlchemy
import warnings
warnings.filterwarnings('ignore')


app = Flask(__name__)
userName = os.getenv('mysql_user')
password = os.getenv('mysql_pass')
host = os.getenv('mysql_host')
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{userName}:{password}@{host}:3306/IngreScan'
db_obj = SQLAlchemy(app)

UPLOAD_FOLDER = 'tmp/test/data/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

[food_rec_model_global, knn_nutrition_model_global, nutrition_data_df_global] = api_config_init()


@app.route('/user', methods=['GET'])
def get_all_users():
    users = user_data.query.all()
    output = []
    for user in users:
        userData = {'public_id': user.public_id, 'fname': user.u_fname, 'lname': user.u_lname, 'password': user.u_pwd}
        output.append(userData)

    return jsonify({'users': output})


@app.route('/user/<public_id>', methods=['GET'])
def get_user(public_id):
    user = user_data.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify({'message': 'No user found!'})

    userData = {'public_id': user.public_id, 'fname': user.u_fname, 'lname': user.u_lname, 'password': user.u_pwd}
    return jsonify({'user': userData})


@app.route('/signup', methods=['POST'])
def register_user():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    public_id = str(uuid.uuid4())
    new_user = user_data(public_u_id=public_id, u_fname=data['fname'], u_lname=data['lname'], u_phone=data['phone'], u_email=data['email'], u_pwd=hashed_password)
    db_obj.session.add(new_user)
    db_obj.session.commit()

    return jsonify({'message': 'New user created!', 'id': public_id})


@app.route('/login')
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Login required!'})
    user = user_data.query.filter_by(u_email=auth.username).first()
    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Login required!'})
    if check_password_hash(user.password, auth.password):
        return jsonify({'message': 'The user has been logged in!', 'id': user.public_id})

    return make_response('Could not verify', 401, {'WWW-Authenticate': 'Login required!'})

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/imageUpload', methods=['POST'])
def upload():
    public_id = request.form['id']
    image = request.files['image']
    if not image:
        return 'No image uploaded!', 400

    if image and allowed_file(image.filename):
        filename = secure_filename(image.filename)
        basedir = os.path.abspath(os.path.dirname(__file__))
        image.save(os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename))
        mimetype = image.mimetype
        if not filename or not mimetype:
            return 'Bad upload!', 400

        img = open_image(os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename))

        predicted_food_item = food_predict(food_rec_model_global, img)
        food_description = get_nutrition_info(nutrition_data_df_global, predicted_food_item)

        if len(list(food_description.keys())) > 0:
            recommended_food_items = recommend_food(nutrition_data_df_global, knn_nutrition_model_global, food_description)

        response = {
            # "food_item": food_description['food_item'],
            "energy_100g": food_description['energy_100g'],
            "carbohydrates_100g": food_description['carbohydrates_100g'],
            "proteins_100g": food_description['proteins_100g'],
            "fat_100g": food_description['fat_100g'],
            "fiber_100g": food_description['fiber_100g'],
            "cholesterol_100g": food_description['cholesterol_100g'],
            "recommended_food_items": recommended_food_items
        }
        # userFoodData = user_food_data(public_u_id = public_id, image=image.read(), foodname=food_description['food_item'], mimetype=mimetype)
        # db_obj.session.add(userFoodData)
        # db_obj.session.commit()

    return response


if __name__ == "__main__":
    app.run(debug=True)

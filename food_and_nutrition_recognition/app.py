import os
from fastai.vision.image import open_image
from flask import Flask, request, jsonify, make_response
from fastai.vision import *
import time
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import uuid
from database.db import connect_to_db
from scripts.utils import api_config_init, food_predict, get_nutrition_info, recommend_food, allowed_file, \
    s3_upload_data
import warnings
warnings.filterwarnings('ignore')

app = Flask(__name__)
db_obj = connect_to_db(app)
from database.models import user_data, user_food_data, user_nutrition_history

user_data = user_data
user_food_data = user_food_data
user_nutrition_history = user_nutrition_history
cfg, food_rec_model_global, knn_nutrition_model_global, nutrition_data_df_global = api_config_init()


@app.route('/user', methods=['GET'])
def get_all_users():
    try:
        global user_data
        users = user_data.query.all()
        output = []
        for user in users:
            u_temp = {'public_u_id': user.public_u_id, 'fname': user.u_fname, 'lname': user.u_lname, 'email': user.u_email}
            output.append(u_temp)
        return jsonify({'users': output})
    except Exception as e:
        db_obj.session.rollback()
        return jsonify({'error': e})


@app.route('/user/<public_u_id>', methods=['GET'])
def get_user(public_u_id):
    try:
        global user_data
        user = user_data.query.filter_by(public_u_id=public_u_id).first()
        user_dict = {}
        if not user:
            return jsonify({'message': 'No user found!'})

        user_dict = {'public_u_id': user.public_u_id, 'fname': user.u_fname, 'lname': user.u_lname, 'password': user.u_pwd}
        return jsonify({'user': user_dict})
    except Exception as e:
        db_obj.session.rollback()
        return jsonify({'error': e})


@app.route('/signup', methods=['POST'])
def register_user():
    try:
        data = request.get_json()
        hashed_password = generate_password_hash(data['password'], method='sha256')
        public_u_id = str(uuid.uuid4())
        global user_data
        new_user = user_data(public_u_id=public_u_id, u_fname=data['fname'], u_lname=data['lname'], u_phone=data['phone'],
                             u_email=data['email'], u_pwd=hashed_password)
        db_obj.session.add(new_user)
        db_obj.session.commit()
        return jsonify({'message': 'New user created!', 'id': public_u_id})
    except Exception as e:
        db_obj.session.rollback()
        return jsonify({'error': e})


@app.route('/login', methods=['POST'])
def login():
    try:
        auth = request.authorization
        if not auth or not auth.username or not auth.password:
            return make_response('Could not verify', 401, {'WWW-Authenticate': 'Login required!'})
        user = user_data.query.filter_by(u_email=auth.username).first()
        if not user:
            return make_response('Could not verify', 401, {'WWW-Authenticate': 'Login required!'})
        if check_password_hash(user.u_pwd, auth.password):
            return jsonify({'message': 'The user has been logged in!', 'id': user.public_u_id})
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Login required!'})
    except Exception as e:
        db_obj.session.rollback()
        return jsonify({'error': e})


@app.route('/<uid>/imageUpload', methods=['POST'])
def upload(uid):
    try:
        cfg['curr_user_id'] = uid
        cfg['curr_ts_epoch'] = str(int(time.time()))
        image = request.files['image']
        if not image:
            return jsonify({'message': 'No image uploaded. Please upload an image!'}), 400

        ALLOWED_EXTENSIONS = set(eval(cfg['allowed_extensions']))
        if image and allowed_file(image.filename, ALLOWED_EXTENSIONS):
            cfg['base_dir_path'] = os.path.abspath(os.path.dirname(__file__))
            image_file_name = secure_filename(image.filename)
            image_path = cfg['image_path'].format(cfg['base_dir_path'], image_file_name)
            s3_image_key = cfg['s3_image_key'].format(cfg['curr_user_id'], cfg['curr_ts_epoch'], image_file_name)

            image.save(image_path)
            mimetype = image.mimetype
            if not image_file_name or not mimetype:
                return 'Bad upload!', 400

            img = open_image(image)
            predicted_food_item = food_predict(food_rec_model_global, img)
            if len(predicted_food_item) == 0:
                return jsonify({'message': 'Picture not clear. Please click clear picture of the food item.'})

            food_description = get_nutrition_info(nutrition_data_df_global, predicted_food_item)
            if len(list(food_description.keys())) <= 1:
                return jsonify({'message': 'Picture not clear. Please click clear picture of the food item.'})

            userFoodData = user_food_data(public_u_id=cfg['curr_user_id'],
                                          image=os.path.join(cfg['s3'], cfg['bucket'], s3_image_key),
                                          foodname=predicted_food_item, mimetype=mimetype,
                                          timestamp=cfg['curr_ts_epoch'])
            db_obj.session.add(userFoodData)
            db_obj.session.commit()

            userNutritionData = user_nutrition_history(f_id=userFoodData.f_id,
                                                       public_u_id=cfg['curr_user_id'],
                                                       energy_100g=food_description['energy_100g'],
                                                       carbohydrates_100g=food_description['carbohydrates_100g'],
                                                       sugars_100g=food_description['sugars_100g'],
                                                       proteins_100g=food_description['proteins_100g'],
                                                       fat_100g=food_description['fat_100g'],
                                                       fiber_100g=food_description['fiber_100g'],
                                                       cholesterol_100g=food_description['cholesterol_100g'],
                                                       timestamp=cfg['curr_ts_epoch'])
            db_obj.session.add(userNutritionData)
            db_obj.session.commit()

            with db_obj.get_engine().connect() as conn:
                res = conn.execute("""SELECT SUM(`energy_100g`) AS energy,
                SUM(`carbohydrates_100g`) as carbohydrates,
                SUM(`proteins_100g`) as proteins,
                SUM(`fat_100g`) as fat,
                SUM(`fiber_100g`) as fiber,
                SUM(`cholesterol_100g`) as cholesterol
                FROM `IngreScan`.`user_nutrition_history`
                WHERE UNIX_TIMESTAMP(FROM_UNIXTIME(`timestamp`)) > UNIX_TIMESTAMP(CURRENT_DATE()) 
                AND UNIX_TIMESTAMP(FROM_UNIXTIME(`timestamp`)) < UNIX_TIMESTAMP(CURRENT_DATE() + INTERVAL 1 DAY);""")

            user_history = []
            for row in res.first():
                user_history.append(row)

            recommended_food_items = recommend_food(nutrition_data_df_global, knn_nutrition_model_global, user_history)

            response = {
                "food": predicted_food_item,
                "energy_100g": food_description['energy_100g'],
                "carbohydrates_100g": food_description['carbohydrates_100g'],
                "sugars_100g": food_description['sugars_100g'],
                "proteins_100g": food_description['proteins_100g'],
                "fat_100g": food_description['fat_100g'],
                "fiber_100g": food_description['fiber_100g'],
                "cholesterol_100g": food_description['cholesterol_100g'],
                "recommended_food_items": recommended_food_items
            }

            s3_upload_data(cfg['bucket'], s3_image_key, image_path)
            os.remove(image_path)
            return response
    except Exception as e:
        db_obj.session.rollback()
        return jsonify({'error': e})


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

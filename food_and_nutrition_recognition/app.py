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
        return make_response(jsonify({'users': output}), 200)
    except Exception as e:
        db_obj.session.rollback()
        return make_response('Internal Server Error', 500, {'Error': str(e)})


@app.route('/user/<public_u_id>', methods=['GET'])
def get_user(public_u_id):
    try:
        global user_data
        user = user_data.query.filter_by(public_u_id=public_u_id).first()
        user_dict = {}
        if not user:
            return make_response('User not found', 404)

        user_dict = {'public_u_id': user.public_u_id, 'fname': user.u_fname, 'lname': user.u_lname, 'password': user.u_pwd}
        return make_response(jsonify({'user': user_dict}), 200)
    except Exception as e:
        db_obj.session.rollback()
        return make_response('Internal Server Error', 500, {'Error': str(e)})


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
        return make_response(jsonify({'message': 'New user created!', 'id': public_u_id}), 200)
    except Exception as e:
        db_obj.session.rollback()
        return make_response('Internal Server Error', 500, {'Error': str(e)})


@app.route('/login', methods=['POST'])
def login():
    try:
        auth = request.authorization
        if not auth or not auth.username or not auth.password:
            return make_response('Fields can not be empty.', 401, {'WWW-Authenticate': 'Username or Password empty'})
        user = user_data.query.filter_by(u_email=auth.username).first()
        if not user:
            return make_response('Username not found. Please signup as a new user.', 401,
                                 {'WWW-Authenticate': 'Wrong Username'})
        if check_password_hash(user.u_pwd, auth.password):
            return jsonify({'message': 'The user has been logged in!', 'id': user.public_u_id})
        return make_response('Invalid Credentials', 401, {'WWW-Authenticate': 'Wrong Password'})
    except Exception as e:
        db_obj.session.rollback()
        return make_response('Internal Server Error', 500, {'Error': str(e)})


@app.route('/<uid>/imageUpload', methods=['POST'])
def upload(uid):
    try:
        if len(uid) == 0:
            return make_response('Could not verify', 401, {'WWW-Authenticate': 'Login required!'})
        cfg['curr_user_id'] = uid
        cfg['curr_ts_epoch'] = str(int(time.time()))
        image = request.files['image']
        if not image:
            return make_response('No file found. Please upload an image file.', 406)

        ALLOWED_EXTENSIONS = set(eval(cfg['allowed_extensions']))
        if not allowed_file(image.filename, ALLOWED_EXTENSIONS):
            return make_response('Only ' + cfg['allowed_extensions'][1:-1] + ' files supported. '
                                 + "'" + image.filename.split('.')[-1] + "'" + ' file not supported.', 415)

        cfg['base_dir_path'] = os.path.abspath(os.path.dirname(__file__))
        image_file_name = secure_filename(image.filename)
        image_path = cfg['image_path'].format(cfg['base_dir_path'], image_file_name)
        s3_image_key = cfg['s3_image_key'].format(cfg['curr_user_id'], cfg['curr_ts_epoch'], image_file_name)

        image.save(image_path)
        mimetype = image.mimetype
        if not image_file_name or not mimetype:
            return make_response('Bad file upload.', 400)

        img = open_image(image)
        predicted_food_item = food_predict(food_rec_model_global, img)
        if len(predicted_food_item) == 0:
            return make_response('Picture not clear. Please click clear picture of the food item.', 406)

        food_description = get_nutrition_info(nutrition_data_df_global, predicted_food_item)
        if len(list(food_description.keys())) <= 1:
            return make_response('Picture not clear. Please click clear picture of the food item.', 406)

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
            "energy": food_description['energy_100g'],
            "carbohydrates": food_description['carbohydrates_100g'],
            "sugars": food_description['sugars_100g'],
            "proteins": food_description['proteins_100g'],
            "fat": food_description['fat_100g'],
            "fiber": food_description['fiber_100g'],
            "cholesterol": food_description['cholesterol_100g'],
            "recommended_food_items": recommended_food_items,
            "S3_Image_URI": 'https://ingrescan.s3.us-east-2.amazonaws.com/' +
                            s3_image_key.replace('=', '%3D'),
            "mime_type": mimetype
        }

        s3_upload_data(cfg['bucket'], s3_image_key, image_path, mimetype)
        os.remove(image_path)
        return make_response(response, 200)
    except Exception as e:
        db_obj.session.rollback()
        return make_response('Internal Server Error', 500, {'Error': str(e)})


@app.route('/<uid>/userHistory', methods=['GET'])
def get_user_hist(uid):
    try:
        if len(uid) == 0:
            return make_response('Could not verify', 401, {'WWW-Authenticate': 'Login required!'})
        cfg['curr_user_id'] = uid

        with db_obj.get_engine().connect() as conn:
            res = conn.execute(f"""SELECT `ufd`.`foodname` AS food,
            `ufd`.`image` AS S3_Image_URI,
            `ufd`.`mimetype` AS mimetype,
            `energy_100g` AS energy,
            `carbohydrates_100g` AS carbohydrates,
            `sugars_100g` AS sugars,
            `proteins_100g` AS proteins,
            `fat_100g` AS fat,
            `fiber_100g` AS fiber,
            `cholesterol_100g` AS cholesterol,
            FROM_UNIXTIME(unh.`timestamp`) AS `timestamp`
            FROM `IngreScan`.`user_nutrition_history` AS unh
            NATURAL JOIN `IngreScan`.`user_food_data` as ufd
            WHERE UNIX_TIMESTAMP(FROM_UNIXTIME(unh.`timestamp`)) > UNIX_TIMESTAMP(CURRENT_DATE())
                AND UNIX_TIMESTAMP(FROM_UNIXTIME(unh.`timestamp`)) < UNIX_TIMESTAMP(CURRENT_DATE() + INTERVAL 1 DAY)
                AND unh.`public_u_id` = '{uid}';""")

            user_history = []
            keys = list(res.keys())
            for row in res.fetchall():
                temp_dict = {}
                i = 0
                for key in keys:
                    if key == 'S3_Image_URI':
                        temp_dict[key] = 'https://ingrescan.s3.us-east-2.amazonaws.com/' + \
                                  row[i].replace('=', '%3D').split('ingrescan/')[1]
                    else:
                        temp_dict[key] = row[i]
                    i += 1
                user_history.append(temp_dict)
        return make_response({'user_history': user_history}, 200)
    except Exception as e:
        db_obj.session.rollback()
        return make_response('Internal Server Error', 500, {'Error': str(e)})


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

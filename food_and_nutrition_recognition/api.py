from flask import Flask ,request, jsonify, make_response
from fastai.vision import *
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import uuid
from database.db import db_init, db_obj
from database.models import *
from scripts.utils import api_config_init, food_predict, get_nutrition_info, recommend_food
import warnings
warnings.filterwarnings('ignore')


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ingredientsscanner.db'
db_init(app)
[food_rec_model_global, knn_nutrition_model_global, nutrition_data_df_global] = api_config_init()


@app.route('/user', methods=['GET'])
def get_all_users():

    users = User.query.all()
    output = []
    for user in users:
        user_data = {'public_id': user.public_id, 'name': user.name, 'password': user.password}
        output.append(user_data)

    return jsonify({'users': output})


@app.route('/user/<public_id>', methods=['GET'])
def get_user(public_id):
    user = User.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify({'message': 'No user found!'})

    user_data = {'public_id': user.public_id, 'name': user.name, 'password': user.password}
    return jsonify({'user': user_data})


@app.route('/signup', methods=['POST'])
def register_user():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    public_id = str(uuid.uuid4())
    new_user = User(public_id=public_id, name=data['name'], password=hashed_password)
    db_obj.session.add(new_user)
    db_obj.session.commit()

    return jsonify({'message': 'New user created!', 'id': public_id})


@app.route('/login')
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Login required!'})
    user = User.query.filter_by(name=auth.username).first()
    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Login required!'})
    if check_password_hash(user.password, auth.password):
        return jsonify({'message': 'The user has been logged in!'})

    return make_response('Could not verify', 401, {'WWW-Authenticate': 'Login required!'})


@app.route('/imageUpload', methods=['POST'])
def upload():
    image = request.files['image']
    if not image:
        return 'No image uploaded!', 400

    filename = secure_filename(image.filename)
    mimetype = image.mimetype
    if not filename or not mimetype:
        return 'Bad upload!', 400

    # Read the image via file.stream
    img = open_image(filename)

    predicted_food_item = food_predict(food_rec_model_global, img)
    food_description = get_nutrition_info(nutrition_data_df_global, predicted_food_item)

    if len(list(food_description.keys())) > 0:
        recommended_food_items = recommend_food(nutrition_data_df_global, knn_nutrition_model_global, food_description)

    # build response
    response = {
        "food_item": food_description['food_item'],
        "energy_100g": food_description['energy_100g'],
        "recommended_food_items": recommended_food_items
    }
    img = Img(img=image.read(), name=filename, mimetype=mimetype)
    db_obj.session.add(img)
    db_obj.session.commit()

    return response


if __name__ == "__main__":
    app.run(debug=True)

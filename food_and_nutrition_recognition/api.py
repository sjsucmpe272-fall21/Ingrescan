from flask import Flask ,request, jsonify, make_response
from PIL import Image
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import uuid

from database.db import db_init, db
from database.models import *

from scripts.utils import initialize, food_predict, get_nutrition_info, recommend_food

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ingredientsscanner.db'
db_init(app)

@app.route('/user', methods=['GET'])
def get_all_users():

    # if not current_user.admin:
    #     return jsonify({'message' : 'Cannot perform this function!'})

    users = User.query.all()

    output = []

    for user in users:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['name'] = user.name
        user_data['password'] = user.password
        user_data['admin'] = user.admin
        output.append(user_data)

    return jsonify({'users' : output})

@app.route('/user/<public_id>', methods=['GET'])
def get_user(public_id):

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message' : 'No user found!'})

    user_data = {}
    user_data['public_id'] = user.public_id
    user_data['name'] = user.name
    user_data['password'] = user.password
    user_data['admin'] = user.admin

    return jsonify({'user' : user_data})

@app.route('/user', methods=['POST'])
def register_user():
    data = request.get_json()

    hashed_password = generate_password_hash(data['password'], method='sha256')
    public_id=str(uuid.uuid4())
    new_user = User(public_id = public_id, name=data['name'], password=hashed_password, admin=False)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message' : 'New user created!', 'id' : public_id})

@app.route('/user/<public_id>', methods=['PUT'])
def promote_user(public_id): 
    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message' : 'No user found!'})

    user.admin = True
    db.session.commit()

    return jsonify({'message' : 'The user has been promoted!'})

@app.route('/login')
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Login required!'})

    user = User.query.filter_by(name=auth.username).first()

    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Login required!'})

    if check_password_hash(user.password, auth.password):
        loadModels()
        return jsonify({'message' : 'The user has been loggedin!'})
        
    return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Login required!'})

def loadModels():
    [loadModels.food_rec_model, loadModels.knn_nutrition_model, loadModels.nutrition_data_df] = initialize()


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
    img = Image.open(image.stream)

    # Load models
    loadModels()

    predicted_food_item = food_predict(loadModels.food_rec_model, img)
    food_description = get_nutrition_info(loadModels.nutrition_data_df, predicted_food_item)

    if len(list(food_description.keys())) > 0:
        recommended_food_items = recommend_food(loadModels.nutrition_data_df, loadModels.knn_nutrition_model, food_description)

    # build response
    response = {
        "food_item": food_description['food_item'],
        "energy_100g": food_description['energy_100g'],
        "recommended_food_items" : recommended_food_items
    }
    img = Img(img=image.read(), name=filename, mimetype=mimetype)
    db.session.add(img)
    db.session.commit()

    return response


if __name__ == "__main__":
    app.run(debug=True)

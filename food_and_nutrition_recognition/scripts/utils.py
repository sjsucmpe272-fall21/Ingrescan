from configparser import ConfigParser, ExtendedInterpolation
from argparse import ArgumentParser
from fastai.vision import *
import pickle
import pandas as pd
import boto3
import os
from flask_sqlalchemy import SQLAlchemy

s3_client = boto3.client('s3')


def parser():
    arg = ArgumentParser()
    arg.add_argument("-m", "--mode", required=True, help="Mode", choices={"stage", "prod", "test"})
    arg.add_argument("-c", "--config_path", required=True, help="Path of config file")
    return arg


def db_connect(app):
    userName = os.getenv('mysql_user')
    password = os.getenv('mysql_pass')
    host = os.getenv('mysql_host')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{userName}:{password}@{host}:3306/IngreScan'
    return SQLAlchemy(app)


def get_config(mode, config_path):
    cfg = ConfigParser(interpolation=ExtendedInterpolation())
    cfg.read(config_path)
    return dict(cfg.items(mode))


def load_models(food_rec_model_path, knn_nutrition_model_path):
    food_rec_model = load_learner(food_rec_model_path)
    knn_model = pickle.load(open(knn_nutrition_model_path, 'rb'))
    return food_rec_model, knn_model


def load_data(nutrition_data_path):
    nutrition_data = pd.read_csv(nutrition_data_path, header=0)
    return nutrition_data


def allowed_file(filename, ALLOWED_EXTENSIONS):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def api_config_init():
    cfg = get_config('stage', 'config/app.config')
    return init(cfg)


def init(cfg):
    if not os.path.exists(cfg['food_rec_model_path']):
        s3_client.download_file(cfg['bucket'], cfg['food_rec_model_key'], cfg['food_rec_model_path'])
    if not os.path.exists(cfg['knn_nutrition_model_path']):
        s3_client.download_file(cfg['bucket'], cfg['knn_nutrition_model_key'], cfg['knn_nutrition_model_path'])
    if not os.path.exists(cfg['nutrition_data_path']):
        s3_client.download_file(cfg['bucket'], cfg['nutrition_data_key'], cfg['nutrition_data_path'])

    [food_rec_model, knn_nutrition_model] = load_models(cfg['model_path'], cfg['knn_nutrition_model_path'])
    nutrition_data_df = load_data(cfg['nutrition_data_path'])

    return cfg, food_rec_model, knn_nutrition_model, nutrition_data_df


def food_predict(food_rec_model, image):
    image = image.resize((3, 224, 224))
    [predicted_food_item, _, _] = food_rec_model.predict(image)
    return str(predicted_food_item)


def get_nutrition_info(nutrition_data_df, food_item):
    food_item = food_item.replace('_', ' ')
    products = nutrition_data_df['food_item'].unique()

    if food_item not in products:
        return {}

    food_description = nutrition_data_df.loc[nutrition_data_df['food_item'] == food_item].to_dict()
    for key, val in food_description.items():
        food_description[key] = val[next(iter(val))]

    return food_description


def recommend_food(nutrition_data_df, knn_nutrition_model, user_history, n=4):
    distances, indices = knn_nutrition_model.kneighbors([user_history], n_neighbors=n)
    recommended_food = [nutrition_data_df.loc[i]['food_item'] for i in indices[0]]
    return recommended_food


def s3_upload_data(bucket, s3_key, local_path, mime_type):
    try:
        s3_client.upload_file(local_path, bucket, s3_key, ExtraArgs={'ContentType': mime_type, 'ACL': "public-read"})
    except Exception as e:
        print(e)
        return False
    return True

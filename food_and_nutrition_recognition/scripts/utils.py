from configparser import ConfigParser, ExtendedInterpolation
from argparse import ArgumentParser
from fastai.vision import *
import pickle
import pandas as pd
import boto3
import os


def parser():
    arg = ArgumentParser()
    arg.add_argument("-m", "--mode", required=True, help="Mode", choices={"stage", "prod", "test"})
    arg.add_argument("-c", "--config_path", required=True, help="Path of config file")
    return arg


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


def api_config_init():
    return init(get_config('stage', 'config/app.config'))


def init(cfg):
    s3_client = boto3.client('s3')
    s3_client.download_file(cfg['bucket'], cfg['food_rec_model_key'], cfg['food_rec_model_path'])
    s3_client.download_file(cfg['bucket'], cfg['knn_nutrition_model_key'], cfg['knn_nutrition_model_path'])
    s3_client.download_file(cfg['bucket'], cfg['nutrition_data_key'], cfg['nutrition_data_path'])

    [food_rec_model, knn_nutrition_model] = load_models(cfg['model_path'], cfg['knn_nutrition_model_path'])
    nutrition_data_df = load_data(cfg['nutrition_data_path'])

    return food_rec_model, knn_nutrition_model, nutrition_data_df


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


def recommend_food(nutrition_data_df, knn_nutrition_model, user_history, n=3):
    del user_history["food_item"]
    del user_history["sugars_100g"]
    distances, indices = knn_nutrition_model.kneighbors([list(user_history.values())], n_neighbors=n)
    recommended_food = [nutrition_data_df.loc[i]['food_item'] for i in indices[0]]
    return recommended_food

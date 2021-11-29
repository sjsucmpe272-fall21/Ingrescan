from fastai.vision import *
from argparse import ArgumentParser
from scripts.utils import get_config, init, food_predict, get_nutrition_info, recommend_food
import warnings
warnings.filterwarnings('ignore')


def parser():
    arg = ArgumentParser()
    arg.add_argument("-m", "--mode", required=True, help="Mode", choices={"stage", "prod", "test"})
    arg.add_argument("-c", "--config_path", required=True, help="Path of config file")
    return arg


if __name__ == "__main__":
    ap = parser()
    args_dict = vars(ap.parse_args())

    cfg = get_config(args_dict['mode'], args_dict['config_path'])
    [food_rec_model, knn_nutrition_model, nutrition_data_df] = init(cfg)
    img = open_image(cfg['test_image_path'])
    predicted_food_item = food_predict(food_rec_model, img)
    food_description = get_nutrition_info(nutrition_data_df, predicted_food_item)
    print("Food Description: ", food_description)

    if len(list(food_description.keys())) > 0:
        recommended_food_items = recommend_food(nutrition_data_df, knn_nutrition_model, food_description)
        print("Recommended Food: ", recommended_food_items)

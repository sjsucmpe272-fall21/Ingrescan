#!/bin/bash -l

cd /home/ubuntu/ingrescan/Ingrescan/food_and_nutrition_recognition/
conda activate ingrescan

echo "running ingrescan"
python api.py

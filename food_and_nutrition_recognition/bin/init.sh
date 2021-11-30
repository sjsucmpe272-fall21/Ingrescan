#!/bin/bash

# init.sh - to be run as "ubuntu" user
#source ~/.bashrc

# CONDA_PREFIX contains the location of conda install
cd /ingrescan/Ingrescan/
git fetch && git checkout food_and_nutritions_recognition
git pull origin food_and_nutritions_recognition

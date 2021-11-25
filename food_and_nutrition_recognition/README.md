# Food & Nutrition Recognition and Food Recommendation

Given food image, recognise the food item, its nutrition information and recommend other food items based on user's history of food consumption.

## Getting Started

Make sure *app.config* is set with all mandatory parameters with right values along with the following external dependencies:

- Python with conda is installed. Refer to [this link](https://medium.com/@GalarnykMichael/setting-up-pycharm-with-anaconda-plus-installing-packages-windows-mac-db2b158bd8c) to setup for conda with python.

- Make sure AWS is setup on local. Refer to [this link (till Step 4: CLI Setup)](https://aws.amazon.com/blogs/quantum-computing/setting-up-your-local-development-environment-in-amazon-braket/) for details. The aws account configured should have access to:
  1. s3 location access for - 'ingrescan' 

#### Setup
On the terminal, run the following commands sequentially:
```
git clone git@github.com:sjsucmpe272-fall21/Ingrescan.git
cd Ingrescan/food_and_nutrition_recognition
conda env create -f environment.yml
conda activate ingrescan
```

## How to Use

#### Help
```bash
python -m  test -h
```

```bash
usage: test.py [-h] -m {test,prod,stage} -c CONFIG_PATH

optional arguments:
  -h, --help            show this help message and exit
  -m {test,prod,stage}, --mode {test,prod,stage}
                        Mode
  -c CONFIG_PATH, --config_path CONFIG_PATH
                        Path of config file
```

#### Running main code
Format of command to run:
```bash
python -m test -m <MODE> -c <CONFIG_PATH>
```
EXAMPLE COMMAND:
```bash
python -m main -m test -c config/app.config
```

Miscellaneous Notes
--------------------
#### Data storage details
Data is stored in the following s3 location in bucket - **ingrescan**:

1. ingrescan/uno/model/
2. ingrescan/uno/data/

import argparse
import os
import shutil
from tqdm import tqdm
import logging
from src.utils.common_utils import read_yaml, create_directories, load_image_data
from src.utils.model import load_model
from src.stage_01_get_data import get_data
from src.stage_02_prepare_base_model import prepare_base_model
from src.stage_03_prepare_callback import prepare_callbacks
from src.utils.call_backs import get_callbacks

import random


STAGE = "STAGE_NAME" ## <<< change stage name 

logging.basicConfig(
    filename=os.path.join("logs", 'running_logs.log'), 
    level=logging.INFO, 
    format="[%(asctime)s: %(levelname)s: %(module)s]: %(message)s",
    filemode="a"
    )


def train_model(config_path, params_path):
    ## read config files
    get_data(config_path)
    prepare_base_model(config_path, params_path)
    prepare_callbacks(config_path)
    
    config = read_yaml(config_path)
    params = read_yaml(params_path)
    artifacts_dir = config["artifacts"]["ARTIFACTS_DIR"]
    callback_dir = config["artifacts"]["CALLBACKS_DIR"]
    callback_dir_path = os.path.join(artifacts_dir, callback_dir)
    callbacks = get_callbacks(callback_dir_path)

    artifacts_dir = config["artifacts"]["ARTIFACTS_DIR"]
    base_model_dir = config["artifacts"]["BASE_MODEL_DIR"]
    base_model_dir_path = os.path.join(artifacts_dir, base_model_dir)
    untrained_model_dir_path = os.path.join(base_model_dir_path)
    train_model_dir = config["artifacts"]["TRAINED_MODEL_DIR"]
    train_model_dir_path = os.path.join(train_model_dir, 'trained_model.h5')
    data_path = 'data'
    train_ds, val_ds = load_image_data(data_path, params)
    model = load_model(untrained_model_dir_path, config)
    model.fit(train_ds, epochs=params["EPOCHS"], callbacks=callbacks, validation_data=val_ds)
    model.save(train_model_dir_path)


if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument("--config", "-c", default="configs/config.yaml")
    args.add_argument("--params", "-p", default="params.yaml")
    parsed_args = args.parse_args()

    try:
        logging.info("\n********************")
        logging.info(f">>>>> stage {STAGE} started <<<<<")
        train_model(config_path=parsed_args.config, params_path=parsed_args.params)
        logging.info(f">>>>> stage {STAGE} completed!<<<<<\n")
    except Exception as e:
        logging.exception(e)
        raise e
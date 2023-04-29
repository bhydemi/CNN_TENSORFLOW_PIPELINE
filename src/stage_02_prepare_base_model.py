import argparse
import os
import shutil
from tqdm import tqdm
import logging
from src.utils.common_utils import read_yaml, create_directories
from src.utils.model import get_base_model, prepare_full_model
import random
import tensorflow as tf


STAGE = "TWO" ## <<< change stage name 

logging.basicConfig(
    filename=os.path.join("logs", 'running_logs.log'), 
    level=logging.INFO, 
    format="[%(asctime)s: %(levelname)s: %(module)s]: %(message)s",
    filemode="a"
    )


def prepare_base_model(config_path, params_path):
    ## read config files
    config = read_yaml(config_path)
    params = read_yaml(params_path)
    artifacts_dir = config["artifacts"]["ARTIFACTS_DIR"]
    base_model_dir = config["artifacts"]["BASE_MODEL_DIR"]
    base_model_dir_path = os.path.join(artifacts_dir, base_model_dir)
    create_directories([base_model_dir_path])

    base_model = get_base_model(params)
    full_model = prepare_full_model(base_model, params)

    updated_base_model_path = os.path.join(base_model_dir_path, config["artifacts"]["UPDATED_BASE_MODEL_NAME"])

    full_model.save(updated_base_model_path)


if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument("--config_path", "-c", default="configs/config.yaml")
    args.add_argument("--params_path", "-p", default="params.yaml")
    parsed_args = args.parse_args()

    try:
        logging.info("\n********************")
        logging.info(f">>>>> stage {STAGE} started <<<<<")
        prepare_base_model(config_path=parsed_args.config_path, params_path=parsed_args.params_path)
        logging.info(f">>>>> stage {STAGE} completed!<<<<<\n")
    except Exception as e:
        logging.exception(e)
        raise e
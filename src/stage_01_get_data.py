import argparse
import os
import shutil
from tqdm import tqdm
import logging

import sys

sys.path.append("/path/to/src")

import src.utils.common_utils as utils
#from src.utils.common_utils import create_directories, read_yaml
import random


STAGE = "GET DATA"

logging.basicConfig(
    filename=os.path.join("logs", 'running_logs.log'), 
    level=logging.INFO, 
    format="[%(asctime)s: %(levelname)s: %(module)s]: %(message)s",
    filemode="a"
    )


def get_data(config_path):
    config = utils.read_yaml(config_path)
    remote_data_path = config["data_source"]
    local_data_path = config["data_local"]
    utils.create_directories([local_data_path])
    for data_dir in tqdm(os.listdir(remote_data_path), colour="green"):
        data_dir_path = os.path.join(remote_data_path, data_dir)
        if os.path.isdir(data_dir_path):
            for f in tqdm(os.listdir(data_dir_path)):
                if f.endswith(".jpg"):
                    shutil.copy(os.path.join(data_dir_path, f), local_data_path)
    return local_data_path


if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument("--config", "-c", default="configs/config.yaml")
    args.add_argument("--params", "-p", default="params.yaml")
    parsed_args = args.parse_args()

    try:
        logging.info("\n********************")
        logging.info(f">>>>> stage {STAGE} started <<<<<")
        get_data(config_path=parsed_args.config)
        logging.info(f">>>>> stage {STAGE} completed!<<<<<\n")
    except Exception as e:
        logging.exception(e)
        raise e
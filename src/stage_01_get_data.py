import argparse
import os
import shutil
from tqdm import tqdm
import logging

import src.utils.common_utils as utils
import random


STAGE = "GET DATA"

logging.basicConfig(
    filename=os.path.join("logs", 'running_logs.log'), 
    level=logging.INFO, 
    format="[%(asctime)s: %(levelname)s: %(module)s]: %(message)s",
    filemode="a"
    )


def get_data(config_path):
    """This function downloads data from remote source and saves it in the local system
    
    Args:
        config_path ([str]): [path to yaml file]
    """
    config = utils.read_yaml(config_path)
    
    source_data_dirs = config["source_download_dirs"]
    local_data_dirs = config["local_data_dirs"]

    N = len(source_data_dirs)
    for source_data_dir, local_data_dir in zip(source_data_dirs, local_data_dirs):
        logging.info(f"Downloading data from {source_data_dir} to {local_data_dir}")
        utils.create_directories([local_data_dir])
        for file in tqdm(os.listdir(source_data_dir)):
            shutil.copy(os.path.join(source_data_dir, file), local_data_dir)
        logging.info(f"Downloaded data from {source_data_dir} to {local_data_dir}")


if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument("--config_path", "-c", default="configs/config.yaml")
    parsed_args = args.parse_args()

    try:
        logging.info("\n********************")
        logging.info(f">>>>> stage {STAGE} started <<<<<")
        get_data(config_path=parsed_args.config_path)
        logging.info(f">>>>> stage {STAGE} completed!<<<<<\n")
    except Exception as e:
        logging.exception(e)
        raise e
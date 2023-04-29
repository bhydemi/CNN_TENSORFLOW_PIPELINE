import argparse
import os
import shutil
from tqdm import tqdm
import logging
import time
from src.utils.common_utils import read_yaml, create_directories
from src.utils.call_backs import (create_and_save_tensorboard_callback,
                                   create_and_save_checkpoint_callback,
                                     create_and_save_early_stopping_callback
)
import random


STAGE = "STAGE_NAME" ## <<< change stage name 

logging.basicConfig(
    filename=os.path.join("logs", 'running_logs.log'), 
    level=logging.INFO, 
    format="[%(asctime)s: %(levelname)s: %(module)s]: %(message)s",
    filemode="a"
    )


def prepare_callbacks(config_path):
    ## read config files
    config = read_yaml(config_path)
    artifacts_dir = config["artifacts"]["ARTIFACTS_DIR"]
    tensorboard_dir = config["artifacts"]["TENSORBOARD_ROOT_LOG_DIR"]
    callback_dir = config["artifacts"]["CALLBACKS_DIR"]
    tensorboard_dir_path = os.path.join(artifacts_dir, tensorboard_dir)
    callback_dir_path = os.path.join(artifacts_dir, callback_dir)
    create_directories([tensorboard_dir_path, callback_dir_path])
    create_and_save_tensorboard_callback(tensorboard_dir_path,callback_dir_path)
    create_and_save_checkpoint_callback(callback_dir_path)
    create_and_save_early_stopping_callback(callback_dir_path)



if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument("--config_path", "-c", default="configs/config.yaml")
    parsed_args = args.parse_args()

    try:
        logging.info("\n********************")
        logging.info(f">>>>> stage {STAGE} started <<<<<")
        prepare_callbacks(config_path=parsed_args.config_path)
        logging.info(f">>>>> stage {STAGE} completed!<<<<<\n")
    except Exception as e:
        logging.exception(e)
        raise e
import os
import yaml
import logging
import time
import pandas as pd
import json
import shutil
import tqdm


def read_yaml(path_to_yaml):
    """This function reads the yaml file and returns the content

    Args:
        path_to_yaml ([str]): [path to yaml file]
    """
    with open(path_to_yaml) as yaml_file:
        content = yaml.safe_load(yaml_file)
    logging.info(f"yaml file: {path_to_yaml} loaded successfully")
    return content


def create_directories(path_to_directories: list):
    """This function creates directories for the given path

    Args:
        path_to_directories (list): [list of paths to create directories]
    """
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        logging.info(f"created directory at: {path}")


def save_json(path: str, data: dict):
    """This function saves the json file at the given path

    Args:
        path (str): [path to save the json file]
        data (dict): [data to be saved in json file]
    """
    with open(path, "w") as f:
        json.dump(data, f, indent=4)
    logging.info(f"json file saved at: {path}")


def copy_files(source: str, destination: str):
    """This function copies files from source to destination

    Args:
        source (str): [source path]
        destination (str): [destination path]
    """
    logging.info(f"Downloading data from {source} to {destination}")
    create_directories([destination])
    for file in tqdm(os.listdir(source)):
        shutil.copy(os.path.join(source, file), destination)
        logging.info(f"Downloaded data from {source} to {destination}")

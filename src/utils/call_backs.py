import tensorflow as tf
import logging
import io
import joblib
import time
import os

def get_timestamp(filename):
    timestamp = time.asctime().replace(" ", "_").replace(":", ".")
    unique_filename = f"{filename}_{timestamp}"
    return unique_filename

def create_and_save_tensorboard_callback(tensorboard_dir_path, callback_dir_path):
    unique_name = get_timestamp("tb_log")
    tensorboard_dir_path = os.path.join(tensorboard_dir_path, unique_name)
    tensorboard =  tf.keras.callbacks.TensorBoard(log_dir=tensorboard_dir_path, histogram_freq=1)
    tensorboard_path = os.path.join(callback_dir_path, "tensorboard.pkl")
    joblib.dump(tensorboard, tensorboard_path)
    logging.info(f"Tensorboard callback saved at {tensorboard_path}")

def create_and_save_checkpoint_callback(checkpoints_dir_path):
    checkpoint_file = os.path.join(checkpoints_dir_path, "model_checkpoint.h5")
    checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(checkpoint_file, save_best_only=True)
    logging.info(f"Checkpoint callback saved at {checkpoint_file}")
    joblib.dump(checkpoint_callback, checkpoint_file)
    logging.info(f"Checkpoint callback saved at {checkpoint_file}")

def create_and_save_early_stopping_callback(callback_dir_path):
    callback = tf.keras.callbacks.EarlyStopping(monitor="val_loss", patience=5)
    callback_path = os.path.join(callback_dir_path, "early_stopping.pkl")
    joblib.dump(callback, callback_path)
    logging.info(f"Early stopping callback saved at {callback_path}")

def get_callbacks(callback_dir_path):
    tensorboard_path = os.path.join(callback_dir_path, "tensorboard.pkl")
    checkpoint_path = os.path.join(callback_dir_path, "model_checkpoint.h5")
    early_stopping_callback = joblib.load(os.path.join(callback_dir_path, "early_stopping.pkl"))
    tensorboard_callback = joblib.load(tensorboard_path)
    checkpoint_callback = joblib.load(checkpoint_path)
    logging.info("Callbacks loaded")
    return [early_stopping_callback, tensorboard_callback, checkpoint_callback]
import tensorflow as tf
import logging
import io
import os


def get_base_model(params):
    base_model = tf.keras.applications.ResNet101(
        weights="imagenet",
        input_shape=(params["IMAGE_SIZE"], params["IMAGE_SIZE"], 3),
        include_top=False,
    )
    return base_model

def prepare_full_model(base_model, params, freeze_base_model=True, freeze_till=None):
    """
        prepare full model by adding flatten and dense layer on top of base model

        args:
            base_model: base model
            params: parameter dictionary
            freeze_base_model: if True, freeze all the layers of base model
            freeze_till: if freeze_base_model is False, freeze all the layers of base model till freeze_till index

        return:
            model: full model
    """
    if freeze_base_model:
        for layer in base_model.layers:
            layer.trainable = False
    elif (freeze_till is not None) and (freeze_till > 0):
        for layer in base_model.layers[:freeze_till]:
            layer.trainable = False
        for layer in base_model.layers[freeze_till:]:
            layer.trainable = True
    flatten = tf.keras.layers.Flatten()(base_model.output)
    prediction = tf.keras.layers.Dense(params["CLASSES_COUNT"], activation="softmax")(flatten)
    model = tf.keras.models.Model(inputs=base_model.input, outputs=prediction)

    model.compile(optimizer='sgd', loss=params['LOSS'], metrics=params['METRICS'])
    logging.info("compilation of model is done")
    
    def __get_model_summary(model):
        with io.StringIO() as stream:
            model.summary(print_fn=lambda x: stream.write(f"{x}\n"))
            summary_string = stream.getvalue()
        return summary_string
    
    logging.info(f"model summary: \n {__get_model_summary(model)}")

    return model

def load_model(model_path, config):
    model = os.path.join(model_path, config['artifacts']['UPDATED_BASE_MODEL_NAME'])
    model = tf.keras.models.load_model(model)
    return model
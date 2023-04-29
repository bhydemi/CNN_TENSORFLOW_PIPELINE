import tensorflow as tf


def get_base_model(params):
    base_model = tf.keras.applications.ResNet50(
        weights="imagenet",
        input_shape=(params["IMAGE_SIZE"], params["IMAGE_SIZE"], 3),
        include_top=False,
    )
    return base_model

def prepare_full_model(base_model, params):
    base_model.trainable = False
    model = tf.keras.Sequential([
        base_model,
        tf.keras.layers.GlobalAveragePooling2D(),
        tf.keras.layers.Dense(1024, activation='relu'),
        tf.keras.layers.Dense(params['CLASSES_COUNT'], activation='softmax')
    ])

    return model
import tensorflow as tf


# ConvNet模型
def ConvNet(img_height=96, img_width=96, num_classes=2, steps_per_epoch=100):
    model = tf.keras.models.Sequential([
        tf.keras.layers.Rescaling(1./255, input_shape=(img_height, img_width, 3)),
        # tf.keras.layers.Rescaling(1./127.5, offset=-1, input_shape=(img_height, img_width, 3)),
        tf.keras.layers.Conv2D(4, 3, strides=(2, 2), activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.001)),
        tf.keras.layers.MaxPool2D(pool_size=(2, 2), strides=(2, 2)),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dropout(0.25),
        tf.keras.layers.Dense(num_classes)
    ])

    lr_schedule = tf.keras.optimizers.schedules.InverseTimeDecay(0.001, 
                                                                 decay_steps=steps_per_epoch*10, 
                                                                 decay_rate=1, 
                                                                 staircase=False)

    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=lr_schedule),
                  loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                  metrics=["accuracy"])
    
    return model


# FireNet_v1模型
def FireNet_v1(img_height=64, img_width=64, num_classes=2, steps_per_epoch=100):
    # NHWC
    model = tf.keras.models.Sequential([
        tf.keras.layers.Rescaling(1./255, input_shape=(img_height, img_width, 3)),
        tf.keras.layers.Conv2D(16, 3, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.001)),
        tf.keras.layers.AveragePooling2D(),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Conv2D(32, 3, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.001)),
        tf.keras.layers.AveragePooling2D(),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Conv2D(64, 3, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.001)),
        tf.keras.layers.AveragePooling2D(),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(256, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.001)),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(128, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.001)),
        tf.keras.layers.Dense(num_classes, activation='softmax')
    ])

    lr_schedule = tf.keras.optimizers.schedules.InverseTimeDecay(0.00051, 
                                                                 decay_steps=steps_per_epoch*1000, 
                                                                 decay_rate=1, 
                                                                 staircase=False)

    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=lr_schedule),
                  loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                  metrics=["accuracy"])
    
    return model


# FireNet_v2模型
def FireNet_v2(img_height=64, img_width=64, num_classes=2, steps_per_epoch=96):
    # NHWC
    model = tf.keras.models.Sequential([
        tf.keras.layers.Rescaling(1./255, input_shape=(img_height, img_width, 3)),
        tf.keras.layers.Conv2D(15, 3, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.001)),
        tf.keras.layers.AveragePooling2D(),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Conv2D(20, 3, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.001)),
        tf.keras.layers.AveragePooling2D(),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Conv2D(30, 3, activation='sigmoid', kernel_regularizer=tf.keras.regularizers.l2(0.001)),
        tf.keras.layers.AveragePooling2D(),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(256, activation='sigmoid', kernel_regularizer=tf.keras.regularizers.l2(0.001)),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(128, activation='sigmoid', kernel_regularizer=tf.keras.regularizers.l2(0.001)),
        tf.keras.layers.Dense(num_classes, activation='softmax')
    ])

    lr_schedule = tf.keras.optimizers.schedules.InverseTimeDecay(0.00051, 
                                                                 decay_steps=steps_per_epoch*1000, 
                                                                 decay_rate=1, 
                                                                 staircase=False)

    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=lr_schedule),
                  loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                  metrics=["accuracy"])
    
    return model


# Alexnet模型
def AlexNet(img_height=224, img_width=224, num_classes=1000):
    # tensorflow中的tensor通道排序是NHWC
    input_image = tf.keras.layers.Input(shape=(img_height, img_width, 3), dtype="float32")  # output(None, 224, 224, 3)
    x = tf.keras.layers.ZeroPadding2D(((1, 2), (1, 2)))(input_image)                      # output(None, 227, 227, 3)
    x = tf.keras.layers.Conv2D(48, kernel_size=11, strides=4, activation="relu")(x)       # output(None, 55, 55, 48)
    x = tf.keras.layers.MaxPool2D(pool_size=3, strides=2)(x)                              # output(None, 27, 27, 48)
    x = tf.keras.layers.Conv2D(128, kernel_size=5, padding="same", activation="relu")(x)  # output(None, 27, 27, 128)
    x = tf.keras.layers.MaxPool2D(pool_size=3, strides=2)(x)                              # output(None, 13, 13, 128)
    x = tf.keras.layers.Conv2D(192, kernel_size=3, padding="same", activation="relu")(x)  # output(None, 13, 13, 192)
    x = tf.keras.layers.Conv2D(192, kernel_size=3, padding="same", activation="relu")(x)  # output(None, 13, 13, 192)
    x = tf.keras.layers.Conv2D(128, kernel_size=3, padding="same", activation="relu")(x)  # output(None, 13, 13, 128)
    x = tf.keras.layers.MaxPool2D(pool_size=3, strides=2)(x)                              # output(None, 6, 6, 128)

    x = tf.keras.layers.Flatten()(x)                         # output(None, 6*6*128)
    x = tf.keras.layers.Dropout(0.2)(x)
    x = tf.keras.layers.Dense(2048, activation="relu")(x)    # output(None, 2048)
    x = tf.keras.layers.Dropout(0.2)(x)
    x = tf.keras.layers.Dense(2048, activation="relu")(x)    # output(None, 2048)
    x = tf.keras.layers.Dense(num_classes)(x)                  # output(None, 5)
    predict = tf.keras.layers.Softmax()(x)

    model = tf.keras.models.Model(inputs=input_image, outputs=predict)

    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.0005),
                  loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=False),
                  metrics=["accuracy"])

    return model


def MobileNet(img_height=224, img_width=224, num_classes=1000):
    # tensorflow中的tensor通道排序是NHWC
    input_image = tf.keras.layers.Input(shape=(img_height, img_width, 3), dtype="float32")  # output(None, 224, 224, 3)
    x = tf.keras.layers.ZeroPadding2D(((1, 2), (1, 2)))(input_image)                      # output(None, 227, 227, 3)
    x = tf.keras.layers.Conv2D(48, kernel_size=11, strides=4, activation="relu")(x)       # output(None, 55, 55, 48)
    x = tf.keras.layers.MaxPool2D(pool_size=3, strides=2)(x)                              # output(None, 27, 27, 48)
    x = tf.keras.layers.Conv2D(128, kernel_size=5, padding="same", activation="relu")(x)  # output(None, 27, 27, 128)
    x = tf.keras.layers.MaxPool2D(pool_size=3, strides=2)(x)                              # output(None, 13, 13, 128)
    x = tf.keras.layers.Conv2D(192, kernel_size=3, padding="same", activation="relu")(x)  # output(None, 13, 13, 192)
    x = tf.keras.layers.Conv2D(192, kernel_size=3, padding="same", activation="relu")(x)  # output(None, 13, 13, 192)
    x = tf.keras.layers.Conv2D(128, kernel_size=3, padding="same", activation="relu")(x)  # output(None, 13, 13, 128)
    x = tf.keras.layers.MaxPool2D(pool_size=3, strides=2)(x)                              # output(None, 6, 6, 128)

    x = tf.keras.layers.Flatten()(x)                         # output(None, 6*6*128)
    x = tf.keras.layers.Dropout(0.2)(x)
    x = tf.keras.layers.Dense(2048, activation="relu")(x)    # output(None, 2048)
    x = tf.keras.layers.Dropout(0.2)(x)
    x = tf.keras.layers.Dense(2048, activation="relu")(x)    # output(None, 2048)
    x = tf.keras.layers.Dense(num_classes)(x)                  # output(None, 5)
    predict = tf.keras.layers.Softmax()(x)

    model = tf.keras.models.Model(inputs=input_image, outputs=predict)

    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.0005),
                  loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=False),
                  metrics=["accuracy"])

    return model


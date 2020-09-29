# -*- coding: utf-8 -*-
"""image_classification.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1k-HDg_WIgK-X_DIoi6VwnwwzsA2Xs7xz
"""

import numpy as np
import tensorflow
import os
import matplotlib.pyplot as plt
import cv2
import random
import tensorflow as tf
import keras
from keras import Sequential
from keras.layers import Conv2D, Activation, MaxPooling2D, Flatten, Dense


training_data = []

IMG_DIM = 50

def get_model():
    model = Sequential()
    model.add(Conv2D(256, (3, 3), input_shape=X.shape[1:]))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Conv2D(256, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Flatten())  # this converts our 3D feature maps to 1D feature vectors

    model.add(Dense(64))

    model.add(Dense(1))
    model.add(Activation('sigmoid'))

    model.compile(loss='binary_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])

    return model



def load_data():
    mask_data_path = os.listdir("./mask")
    no_mask_data_path = os.listdir("./no_mask")

    for img in mask_data_path:
        img_arr = cv2.imread(os.path.join("./mask", img), cv2.IMREAD_GRAYSCALE)
        new_array = cv2.resize(img_arr, (IMG_DIM, IMG_DIM))
        training_data.append([new_array, 0])

    for img in no_mask_data_path:
        img_arr = cv2.imread(os.path.join("./no_mask", img), cv2.IMREAD_GRAYSCALE)
        new_array = cv2.resize(img_arr, (IMG_DIM, IMG_DIM))
        training_data.append([new_array, 1])

    # 0 Means Mask in Image
    # 1 Means No mask in Image

    random.shuffle(training_data)

    X = []
    y = []

    for feature, label in training_data:
        X.append(feature)
        y.append(label)

    X = np.array(X).reshape(-1, IMG_DIM, IMG_DIM, 1)  # Flattening
    X = X / 255  # Normalization

    y = np.array(y)

    return X,y


def save_model(model):
    model.save("self_mask-CNN.model")



def predict_image(model):
    test_image_array = cv2.imread(os.path.join("./test2.jpg"), cv2.IMREAD_GRAYSCALE)
    new_array = cv2.resize(test_image_array, (IMG_DIM, IMG_DIM))
    test_numpy_array = np.array(new_array).reshape(-1, IMG_DIM, IMG_DIM, 1)  # Flattening
    test_numpy_array = test_numpy_array / 255
    result = model.predict_classes(test_numpy_array)
    print(result[0])


def load_model():
    return keras.models.load_model("self_mask-CNN.model")


# Train, Save And Evaluate
# X,y = load_data()
# model = get_model()
# model.fit(X, y, batch_size=50, epochs=5, validation_split=0.3)
# save_model(model)
# predict_image(model)


# From Loaded Model
model = load_model()
predict_image(model)


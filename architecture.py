from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers.core import Flatten
from keras.layers.core import Dense
from keras.layers.core import Dropout
from keras.layers.core import Activation
import random
import cv2
from keras.preprocessing.image import ImageDataGenerator
from keras.layers.normalization import BatchNormalization
import numpy as np

from PIL import ImageFile
def createArc():
    ImageFile.LOAD_TRUNCATED_IMAGES = True

    #Initialize the CNN
    classifier = Sequential()
    #Convolution and Max pooling
    classifier.add(Conv2D(32, (3, 3), input_shape = (128, 128, 3),padding="same", activation = 'relu'))
    classifier.add(MaxPooling2D(pool_size=(3, 3)))
    classifier.add(Dropout(0.25))

    # (CONV => RELU) * 2 => POOL
    classifier.add(Conv2D(64, (3, 3), padding="same"))
    classifier.add(Activation("relu"))
    classifier.add(Conv2D(64, (3, 3), padding="same"))
    classifier.add(Activation("relu"))
    classifier.add(MaxPooling2D(pool_size=(2, 2)))
    classifier.add(Dropout(0.25))

    # (CONV => RELU) * 2 => POOL
    classifier.add(Conv2D(128, (3, 3), padding="same"))
    classifier.add(Activation("relu"))
    classifier.add(Conv2D(128, (3, 3), padding="same"))
    classifier.add(Activation("relu"))
    classifier.add(MaxPooling2D(pool_size=(2, 2)))
    classifier.add(Dropout(0.25))
     
    #Flatten
    classifier.add(Flatten())
    classifier.add(Dense(1024))
    classifier.add(Activation("relu"))
    classifier.add(Dropout(0.5))


     
    #Full connection
    classifier.add(Dense(128, activation = 'relu'))
    classifier.add(Dense(2, activation = 'softmax'))
     
    #Compile classifier
    classifier.compile(optimizer = 'adam', loss = 'categorical_crossentropy', metrics = ['accuracy'])

    print(classifier.summary())


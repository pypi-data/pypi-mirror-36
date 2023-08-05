from keras.models import Model

from keras.layers import Input, Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D

from .cnn import CNN

class SimpleCNN(CNN):
    def __init__(self, *args, **kwargs):
        CNN.__init__(self, *args, **kwargs)
        if type(self.input_shape) == type(None):
            self.input_shape = (32, 32, 3)
    
    def create_model(self, num_classes):
        input_layer = Input(shape=self.input_shape)
        conv1 = Conv2D(32, (3, 3), padding='same', activation='relu')(input_layer)
        conv2 = Conv2D(32, (3, 3), activation='relu')(conv1)
        pool1 = MaxPooling2D(pool_size=(2, 2))(conv2)
        drop1 = Dropout(0.25)(pool1)

        conv3 = Conv2D(64, (3, 3), padding='same', activation='relu')(drop1)
        conv4 = Conv2D(64, (3, 3), activation='relu')(conv3)
        pool2 = MaxPooling2D(pool_size=(2, 2))(conv4)
        drop2 = Dropout(0.25)(pool2)

        flat1 = Flatten()(drop2)
        dense1 = Dense(512, activation='relu')(flat1)
        drop3 = Dropout(0.5)(dense1)
        output_layer = Dense(num_classes, activation='softmax')(drop3)

        model = Model(inputs=input_layer, outputs=output_layer)
        return model
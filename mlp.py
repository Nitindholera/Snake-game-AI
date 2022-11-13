from keras.models import Sequential
from keras.layers import Dense, Activation
from keras import initializers
import numpy as np

class neural_network:
    
    def __init__(self):               
        self.brain = Sequential()

        my_init = initializers.initializers_v1.RandomUniform(minval=-1, maxval=1)

        self.brain.add(Dense(120, activation='relu',input_shape= (12,), kernel_initializer=my_init))
        self.brain.add(Dense(120, activation='relu', kernel_initializer=my_init))
        self.brain.add(Dense(120, activation='relu', kernel_initializer=my_init))
        self.brain.add(Dense(4, activation='softmax', kernel_initializer=my_init))

    def print_weights(self):
        x = np.array(self.brain.get_weights())
        print(x[0][0][0])

    def forward_prop(self, inp):
        return self.brain.predict([inp])
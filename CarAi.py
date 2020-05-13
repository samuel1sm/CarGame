from tensorflow import keras
from math import sqrt
import numpy as np
from GameObjects import Car
class CarAi():
    def __init__(self, inputs_size, final_position = (400,400), model_name = "CarAi"):
        self.inputs_size = inputs_size
        self.model_name = model_name
        self.final_position = final_position
        self.model = self.model_builder()
        self.last_predicted = (0,0)

    def model_builder(self):
        model = keras.Sequential()
        model.add(keras.layers.Dense(units=4, activation="tanh", input_dim = (5)))
        model.add(keras.layers.Dense(units=3, activation="tanh"))
        model.add(keras.layers.Dense(units=2, activation="tanh"))
        model.compile(loss='mse', optimizer=keras.optimizers.Adam(lr=0.001))
        return model

    def predict(self, inputs, max_distance):
        self.last_predicted = self.model.predict(np.array([inputs])/ max_distance)
        return self.last_predicted

    def car_train(self, state : Car):

        if state.activated:
            x,y = state.car_center
            x_dp, y_dp = self.final_position
            dist = sqrt((x - x_dp) ** 2 + (y - y_dp) ** 2)
            if dist != 0:
                reward = 1 / dist
            else:
                reward = 1
        else: 
            reward = -1

        inputs = np.array([state.distances])
        self.model.fit(inputs,[self.last_predicted,reward])

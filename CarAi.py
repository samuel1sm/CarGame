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
        visible = keras.layers.Input(shape = (5))
        hidden1 = keras.layers.Dense(units=4, activation="tanh")(visible)
        hidden2 = keras.layers.Dense(units=3, activation="tanh")(hidden1)
        output_aceleracao = keras.layers.Dense(units=1, activation="sigmoid")(hidden2)
        output_rotacao = keras.layers.Dense(units=1, activation="tanh")(hidden2)
        output_merge = keras.layers.concatenate([output_rotacao,output_aceleracao])
        model = keras.Model(inputs= visible, outputs = output_merge)
        model.compile(loss='mse', optimizer=keras.optimizers.Adam(lr=0.001))
        return model

    def predict(self, inputs, max_distance):
        self.last_predicted = self.model.predict(np.array([inputs])/ max_distance)
        return self.last_predicted

    # def calculate_reward(self, distance, max_distance):

    def car_train(self, this_state, next_state, max_distance):

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

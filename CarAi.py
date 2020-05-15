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
        self.y = 0.95
        self.decay_factor = 0.999

    def model_builder(self):
        import os
        lista = os.listdir("episodes")

        if len(lista) == 0:
            visible = keras.layers.Input(shape = (5))
            hidden1 = keras.layers.Dense(units=4, activation="tanh")(visible)
            hidden2 = keras.layers.Dense(units=3, activation="tanh")(hidden1)
            output_aceleracao = keras.layers.Dense(units=1, activation="sigmoid")(hidden2)
            output_rotacao = keras.layers.Dense(units=1, activation="tanh")(hidden2)
            output_merge = keras.layers.concatenate([output_rotacao,output_aceleracao])
            model = keras.Model(inputs= visible, outputs = output_merge)
            model.compile(loss='mse', optimizer=keras.optimizers.Adam(lr=0.001))

        else:
            print(lista[len(lista) -1 ])
            model = keras.models.load_model(f"episodes/{lista[len(lista) -1 ]}")
        return model

    def predict(self, inputs, max_distance):
        self.last_predicted = self.model.predict(np.array([inputs])/ max_distance)
        return self.last_predicted

    def calculate_reward(self, state) -> float:
        distance = state[0]
        position = state[1]
        if not 0 in distance:
            x,y = position
            x_dp, y_dp = self.final_position
            dist = sqrt((x - x_dp) ** 2 + (y - y_dp) ** 2)
            if dist != 0:
                return 1 / dist
            else:
                return 1
        else: 
            return -1

    def car_train(self, this_state, next_state):
        this_reward = self.calculate_reward(this_state)
        next_reward = self.calculate_reward(next_state)
        reward = this_reward + self.y * next_reward

        inputs = np.array([this_state[0]])
        reward = np.array([[reward,reward]])

        print(reward)
        # print(this_reward,next_reward,reward)
        # print("------------------")
        self.model.fit(inputs,reward, epochs=1, verbose=0)

import pickle
import random
import numpy as np
import glob
import csv
from datetime import datetime
from sklearn.preprocessing import MinMaxScaler

import tflearn
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression
from statistics import median, mean

from scene import Scene
from rocket import Rocket
from controller import RocketController
from extras import Vector

"""
Main class for tensorflow MLP models
"""

LR = 1e-3  # learning rate, might want to play around with
cur_time = datetime.now()
test_time = cur_time.strftime('%Y%m%dT%H%M')
scaler = MinMaxScaler()


def get_successful_games():
    list_success = []
    path = "saved_runs\\*.csv"
    for fname in glob.glob(path):
        with open(fname, newline='') as f:
            reader = csv.reader(f)
            row1 = next(reader)  # gets the first line
            if "True" in str(row1):
                list_success.append(fname)
    return list_success


def separate_input_output():
    list_games = get_successful_games()
    X = []
    y = []
    for game in list_games:
        with open(game, 'r') as read_obj:
            csv_reader = csv.reader(read_obj)
            # skip first two rows
            next(csv_reader)
            next(csv_reader)

            for row in csv_reader:
                X.append(format_input(row[:-1]))  # input
                y.append(format_output(row[-1]))  # output
    return X, y


def format_input(row):
    formatted_row = []
    for element in row:
        try:
            formatted_row.append(float(element))
        except ValueError:
            if element == "False":
                formatted_row.append(float(1))
            else:
                formatted_row.append(float(0))
    return formatted_row


def format_output(element):
    if element == "w":
        return [1, 0, 0, 0, 0, 0]
    elif element == " ":
        return [0, 1, 0, 0, 0, 0]
    elif element == "s":
        return [0, 0, 1, 0, 0, 0]
    elif element == "a":
        return [0, 0, 0, 1, 0, 0]
    elif element == "d":
        return [0, 0, 0, 0, 1, 0]
    return [0, 0, 0, 0, 0, 1]


def get_move(move):
    dict_output = {0: 'w', 1: ' ', 2: 's', 3: 'a', 4: 'd', 5: 'p'}
    return dict_output[move]


def neural_network_model(input_size):
    network = input_data(shape=[None, input_size, 1], name='input')

    network = fully_connected(network, 11, activation='relu')
    network = dropout(network, 0.8)  # not sure what this does yet but seemed important

    # network = fully_connected(network, 128, activation='relu')
    # network = dropout(network, 0.8)

    # network = fully_connected(network, 256, activation='relu')
    # network = dropout(network, 0.8)

    # network = fully_connected(network, 512, activation='relu')
    # network = dropout(network, 0.8)

    # network = fully_connected(network, 256, activation='relu')
    # network = dropout(network, 0.8)

    # network = fully_connected(network, 128, activation='relu')
    # network = dropout(network, 0.8)

    network = fully_connected(network, 6, activation='softmax')
    network = regression(network, optimizer='adam', learning_rate=LR, loss='categorical_crossentropy', name='targets')
    model = tflearn.DNN(network, tensorboard_dir='log')
    return model


def train_model(training_data_input, training_data_output, model=False):
    scaler.fit(training_data_input)
    training_data_input = scaler.transform(training_data_input)
    X = np.array([i for i in training_data_input]).reshape(-1, len(training_data_input[0]), 1)
    y = [i for i in training_data_output]

    if not model:
        model = neural_network_model(input_size=len(X[0]))

    model.fit({'input': X}, {'targets': y}, n_epoch=5, snapshot_step=10, show_metric=True, shuffle=True)
    return model


def show_game(model):
    scores = []
    choices = []

    for _ in range(5):  # number of games you would like to see (one after the other)
        scene = Scene(1000, 1000, init_target_val='random')
        rocket = Rocket(scene, start_pos='air_center')
        controller = RocketController(rocket, physical_control=False)
        cur_frame = 0

        while (True):
            cur_frame += 1
            if cur_frame > 60 * 20:
                print('Timeout!')
                rocket.is_dead = True

            if rocket.is_dead:
                scores.append(rocket.score(recalc=True))
                break
            game_state = np.array(rocket.get_data_list()).reshape(1, -1)
            game_state = scaler.transform(game_state)
            game_state = game_state.reshape(-1, 1)
            game_state = game_state.reshape(-1, len(game_state), 1)
            decision = np.argmax(model.predict(game_state))
            choices.append(decision)
            controller.control(get_move(decision))
            rocket.update()
            scene.draw()

    print('choice 0:{}  choice 1:{} choice 2:{} choice 3:{} choice 4:{} choice 5:{}'.format(
        choices.count(0) / len(choices), choices.count(1) / len(choices),
        choices.count(2) / len(choices), choices.count(3) / len(choices), choices.count(4) / len(choices),
        choices.count(5) / len(choices)))
    print('Average Score:', sum(scores) / len(scores))


if __name__ == '__main__':
    train = True  # True if you want to train a model, False if you want to load an already saved one
    model_name = "20210702T1901"  # the name of the model you want to load (if train is True this is ignored)

    list_games = get_successful_games()
    print("Number of games: ", len(list_games))
    training_data_input = separate_input_output()[0]
    training_data_output = separate_input_output()[1]

    if train:
        model = train_model(training_data_input, training_data_output)
        model.save(f'tsfl_models/{test_time}.model')
        pickle.dump(scaler, open(f'tsfl_models/{test_time}_scaler.pkl', 'wb'))
    else:
        model = neural_network_model(input_size=len(training_data_input[0]))
        scaler = pickle.load(open(f'tsfl_models/{model_name}_scaler.pkl', 'rb'))
        model.load(f'tsfl_models/{model_name}.model', weights_only=True)
        show_game(model)

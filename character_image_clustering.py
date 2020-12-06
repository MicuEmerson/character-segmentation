import os
import cv2
import math
import pickle

from minisom import MiniSom
from feature_extraction import get_data

def som_clustering(DIR_NAME, RESULT_DIR_NAME):
    data = get_data(DIR_NAME)
    rows = math.ceil(math.sqrt(5 * math.sqrt(len(data[0]))))
    cols = math.ceil(math.sqrt(5 * math.sqrt(len(data[0]))))  # sqrt(5*sqrt(N))
    input_len = len(data[0])

    # generate som
    som = MiniSom(rows, cols, input_len, sigma=3, learning_rate=0.7)  # initialization of SOM
    som.train_random(data, 300, True)  # trains the SOM

    with open('som.p', 'wb') as outfile:
        pickle.dump(som, outfile)

    with open('som.p', 'rb') as infile:
        som = pickle.load(infile)
        character_image_names = os.listdir(DIR_NAME)
        dictionary = {}
        for xx, img_name in zip(data, character_image_names):
            cluster = som.winner(xx)  # getting the winner
            if cluster not in dictionary:
                dictionary[cluster] = []
            dictionary[cluster].append(img_name)

    # put in folders
    for (i, j) in dictionary:
        os.mkdir(RESULT_DIR_NAME + str(i) + '-' + str(j))
        for img_name in dictionary[(i, j)]:
            img = cv2.imread(DIR_NAME + img_name)
            cv2.imwrite(RESULT_DIR_NAME + str(i) + '-' + str(j) + '/' + img_name, img)

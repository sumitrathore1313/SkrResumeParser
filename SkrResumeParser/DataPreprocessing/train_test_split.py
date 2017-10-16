import numpy as np

def train_test_split(data):
    train_data = np.array(data[0:int(len(data) * 0.8)])
    test_data = np.array(data[int(len(data) * 0.8):])
    train_x = np.array(list(train_data[:, 0]))
    train_y = np.array(list(train_data[:, 1]))
    test_x = np.array(list(test_data[:, 0]))
    test_y = np.array(list(test_data[:, 1]))

    return train_x, test_x, train_y, test_y
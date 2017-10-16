# Importing the Keras libraries and packages
from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense
import numpy as np

class K1C1HCNN():
    '''
    this model have 1 convolution layer and 1 hidden layer
        this class have three funtions
            training of model CNN()
            testing of model  PCNN()
            validate of model VCNN()
    '''
    def __init__(self, node_input, node_feature = 40, dim_feature = (5, 100),dim_pool = (2, 1), node_h = 100, node_classes = 2, batch_size = 100, epoch = 10):
        '''
        this model accept 2D sentence vector node_input = [?,?]
        2D sentence vecor is matrix of word2vec of each word in sentence
        :param node_input: dimension of input [?, ?]
        :param node_feature: number of feature detector in convolution neural network
        :param dim_feature: number of dimension or size  of feature detector in form of tuple (?, ?)
        :param dim_pool: dimension or size of polling matriz in form if tuple (?, ?)
        :param node_h: number of node in hidden layer in ANN after covolutiion and pooling layer
        :param node_classes: number of classes
        :param batch_size: batch size
        :param epoch: number of epoch
        '''
        self.node_input = node_input
        self.node_feature = node_feature
        self.dim_feature = dim_feature
        self.dim_pool = dim_pool
        self.node_h = node_h
        self.node_classes = node_classes
        self.batch_size = batch_size
        self.epoch = epoch

    def FFNN(self, train_x, train_y, save_model = False):
        '''
        this funtion is used to train model
        :param train_x: training input
        :param train_y: training output
        :param save_model: save model file name
        :return: this funtion return classifier
        '''
        train_x = np.reshape(train_x, [-1, self.node_input[0], self.node_input[1], 1])

        # Initialising the CNN
        classifier = Sequential()

        # Step 1 - Convolution
        classifier.add(Conv2D(self.node_feature, self.dim_feature, input_shape=(self.node_input[0], self.node_input[1], 1), activation='relu'))

        # Step 2 - Pooling
        classifier.add(MaxPooling2D(pool_size=self.dim_pool))

        # Step 3 - Flattening
        classifier.add(Flatten())

        # Step 4 - Full connection
        classifier.add(Dense(units=self.node_h, activation='relu'))
        classifier.add(Dense(units=self.node_classes, activation='softmax'))

        # Compiling the CNN
        classifier.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

        # Fitting the ANN to the Training set
        classifier.fit(train_x, train_y, batch_size=self.batch_size, epochs=self.epoch)

        if save_model:
            pass    # save the model

        return classifier

    def PFFNN(self, classifier, test_x, test_y):
        '''
        this model is used to predict trained model
        :param classifier: trained model classifier which is return from train funtion
        :param test_x: test input
        :param test_y: test output
        :return: this funtion return two value first value is predicted value of test input and second value is accuracy
        '''
        test_x = np.reshape(test_x, [-1, self.node_input[0], self.node_input[1], 1])

        y_pred = classifier.predict(test_x)

        #print("predcition: ", y_pred)
        #print("real value: ", test_y)

        correct = np.equal(np.argmax(y_pred, 1), np.argmax(test_y, 1))
        accuracy = np.mean(correct)
        #print("Accuracy", accuracy)

        return y_pred, accuracy

    def VFFNN(self, validate_x, validate_y):
        '''
        this funtion is used to tuning the hyper parameter of model
        :param validate_x: validate input
        :param validate_y: validate output
        :return:
        '''
        pass

from keras.models import Sequential
from keras.layers import Dense
import numpy as np

class K2HFFNN():
    '''
    this model have 2 hiddeen layer feed foraward network
        this class have three funtions
            training of model FFNN()
            testing of model  PFFNN()
            validate of model VFFNN()
    '''
    def __init__(self, node_input, node_1h = 100, node_2h = 100, node_classes = 2, batch_size = 100, epoch = 10):
        '''
        input vector should be 1D vector mean sentence should be average of word2vec
        :param node_input: dimension of your input vector OR word2vec dimension
        :param node_1h: number of nodes in first hidden layer
        :param node_2h: number of nodes in second hidden layer
        :param node_classes: number of classes in classification
        '''
        self.node_input = node_input
        self.node_1h = node_1h
        self.node_2h = node_2h
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
        # Initialising the ANN
        classifier = Sequential()

        # Adding the input layer and the first hidden layer
        classifier.add(Dense(units=self.node_1h, kernel_initializer='uniform', activation='relu', input_dim=self.node_input))

        # Adding the second hidden layer
        classifier.add(Dense(units=self.node_2h, kernel_initializer='uniform', activation='relu'))

        # Adding the output layer
        classifier.add(Dense(units=self.node_classes, kernel_initializer='uniform', activation='softmax'))

        # Compiling the ANN
        classifier.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

        # Fitting the ANN to the Training set
        classifier.fit(train_x, train_y, batch_size=10, epochs=10)

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

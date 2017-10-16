from VectorProcessing.GloveWordVector import GloveWordVector
from DataPreprocessing.Vocab import get_lexicon
from DataPreprocessing.create_gram_data import get_data
import os
import cPickle as pic
import io
import numpy as np
from sklearn.preprocessing import OneHotEncoder

class GramGloveSentenceVector():

    def __init__(self, path, training = True, dimension = 100, glove_file_path = False, save_word2vec_path = False,
                 save_model_path = False, glove_vocab_file_path = False):
        """
        this class used to create sentence vector
        :param path: give the path of traning or file
        :param traning: False if file is gven
        :param dimension: dimension of glove vector 50,100,200,300
        :param glove_file_path: path of glove vector traning
        :param save_word2vec_path: path of word2vec where it will saved defalut False
        :param save_model_path: path path of saved sen2vec default False
        :param glove_vocab_file_path: path of glove vocab file
        """
        self.traning = training
        self.file_path = path
        if glove_file_path:
            self.glove_file = glove_file_path
            self.glove_vocab_file = glove_vocab_file_path
        else:
            self.glove_file = '/home/sumit/stanford/glove/vector/glove.6B.'+str(dimension)+'d.txt'

        self.save_model = save_model_path

        GWV = GloveWordVector(self.file_path,glove_file_path=self.glove_file, dir=False)
        if save_word2vec_path:
            with open(save_word2vec_path, 'rb') as f:
                self.word2vec, self.vocab, self.ivocab = pic.load(f)
        else:
            self.word2vec, self.vocab, self.ivocab = GWV.get_glove_word_vector()

    def get_3gram_sentenceVector(self):
        sen2vec = []
        if self.traning:
            contents = np.array(get_data(self.file_path))
            training_data = np.array(list(contents[:, 0]))
            output = np.array(list(contents[:, 1]))
            psv = []
            csv = []
            nsv = []
            for i in range(len(training_data)):
                if len(csv):
                    psv = csv[:]
                    csv = nsv[:]
                else:
                    psv = np.zeros(len(self.word2vec[0]), dtype=float)
                    csv = np.zeros(len(self.word2vec[0]), dtype=float)
                    lexicon = get_lexicon(training_data[i])
                    for word in lexicon:
                        csv += self.word2vec[self.vocab[word]]

                if i+1 < len(training_data):
                    nsv = np.zeros(len(self.word2vec[0]), dtype=float)
                    lexicon = get_lexicon(training_data[i+1])
                    for word in lexicon:
                        nsv += self.word2vec[self.vocab[word]]
                else:
                    nsv = np.zeros(len(self.word2vec[0]), dtype=float)
                temp = list(psv)+list(csv)+list(nsv)
                onehotencoder = OneHotEncoder(n_values=9)
                out = onehotencoder.fit_transform(output[i]).toarray()[0]
                sen2vec.append([temp, out])
        else:
            with io.open(self.file_path, 'r', encoding='cp437') as f:
                contents = f.readlines()
                psv = []
                csv = []
                nsv = []
                for i in range(len(contents)):
                    if len(csv):
                        psv = csv[:]
                        csv = nsv[:]
                    else:
                        psv = np.zeros(len(self.word2vec[0]), dtype=float)
                        csv = np.zeros(len(self.word2vec[0]), dtype=float)
                        lexicon = get_lexicon(contents[i])
                        for word in lexicon:
                            csv += self.word2vec[self.vocab[word]]

                    if i + 1 < len(contents):
                        nsv = np.zeros(len(self.word2vec[0]), dtype=float)
                        lexicon = get_lexicon(contents[i + 1])
                        for word in lexicon:
                            nsv += self.word2vec[self.vocab[word]]
                    else:
                        nsv = np.zeros(len(self.word2vec[0]), dtype=float)
                    temp = list(psv) + list(csv) + list(nsv)
                    sen2vec.append(temp)
        if self.save_model:
            pic.dump([sen2vec], open(self.save_model+'sen2vec.p', 'wb'))
        return sen2vec

    def get_5gram_sentenceVector(self):
        sen2vec = []
        if self.traning:
            contents = np.array(get_data(self.file_path))
            training_data = np.array(list(contents[:, 0]))
            output = np.array(list(contents[:, 1]))
            p2sv = []
            psv = []
            csv = []
            nsv = []
            n2sv = []
            for i in range(len(training_data)):
                if len(csv):
                    p2sv = psv[:]
                    psv = csv[:]
                    csv = nsv[:]
                    nsv = n2sv[:]
                else:
                    p2sv = np.zeros(len(self.word2vec[0]), dtype=float)
                    psv = np.zeros(len(self.word2vec[0]), dtype=float)
                    csv = np.zeros(len(self.word2vec[0]), dtype=float)
                    lexicon = get_lexicon(training_data[i])
                    for word in lexicon:
                        csv += self.word2vec[self.vocab[word]]
                    if i + 1 < len(training_data):
                        nsv = np.zeros(len(self.word2vec[0]), dtype=float)
                        lexicon = get_lexicon(training_data[i + 1])
                        for word in lexicon:
                            nsv += self.word2vec[self.vocab[word]]
                    else:
                        nsv = np.zeros(len(self.word2vec[0]), dtype=float)

                if i+2 < len(training_data):
                    n2sv = np.zeros(len(self.word2vec[0]), dtype=float)
                    lexicon = get_lexicon(training_data[i+2])
                    for word in lexicon:
                        n2sv += self.word2vec[self.vocab[word]]
                else:
                    nsv = np.zeros(len(self.word2vec[0]), dtype=float)
                temp = list(p2sv)+list(psv)+list(csv)+list(nsv)+list(n2sv)
                onehotencoder = OneHotEncoder(n_values=9)
                out = onehotencoder.fit_transform(output[i]).toarray()[0]
                sen2vec.append([temp, out])
        else:
            with io.open(self.file_path, 'r', encoding='cp437') as f:
                contents = f.readlines()
                p2sv = []
                psv = []
                csv = []
                nsv = []
                n2sv = []
                for i in range(len(contents)):
                    if len(csv):
                        p2sv = psv[:]
                        psv = csv[:]
                        csv = nsv[:]
                        nsv = n2sv[:]
                    else:
                        p2sv = np.zeros(len(self.word2vec[0]), dtype=float)
                        psv = np.zeros(len(self.word2vec[0]), dtype=float)
                        csv = np.zeros(len(self.word2vec[0]), dtype=float)
                        lexicon = get_lexicon(contents[i])
                        for word in lexicon:
                            csv += self.word2vec[self.vocab[word]]
                        if i + 1 < len(contents):
                            nsv = np.zeros(len(self.word2vec[0]), dtype=float)
                            lexicon = get_lexicon(contents[i + 1])
                            for word in lexicon:
                                nsv += self.word2vec[self.vocab[word]]
                        else:
                            nsv = np.zeros(len(self.word2vec[0]), dtype=float)

                    if i + 2 < len(contents):
                        n2sv = np.zeros(len(self.word2vec[0]), dtype=float)
                        lexicon = get_lexicon(contents[i + 2])
                        for word in lexicon:
                            n2sv += self.word2vec[self.vocab[word]]
                    else:
                        nsv = np.zeros(len(self.word2vec[0]), dtype=float)
                    temp = list(p2sv) + list(psv) + list(csv) + list(nsv) + list(n2sv)
                    sen2vec.append(temp)
        if self.save_model:
            pic.dump([sen2vec], open(self.save_model+'sen2vec.p', 'wb'))
        return sen2vec

if __name__ == '__main__':
    Vector_class = GramGloveSentenceVector('/home/sumit/Desktop/project17/ResumeParser/Data/resume_segments/Level0/all.txt')
    sen2vec = Vector_class.get_3gram_sentenceVector()
    print len(sen2vec)

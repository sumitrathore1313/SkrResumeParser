from VectorProcessing.GloveWordVector import GloveWordVector
from DataPreprocessing.Vocab import get_lexicon
import os
import cPickle as pic
import io
import numpy as np
from sklearn.preprocessing import OneHotEncoder

class GloveSentenceVector():

    def __init__(self, path, dir = True, dimension = 100, glove_file_path = False, save_word2vec_path = False,
                 save_model_path = False, glove_vocab_file_path = False):
        """
        this class used to create sentence vector
        :param path: give the path of dir or file
        :param dir: False if file is gven
        :param dimension: dimension of glove vector 50,100,200,300
        :param glove_file_path: path of glove vector dir
        :param save_word2vec_path: path of word2vec where it will saved defalut False
        :param save_model_path: path path of saved sen2vec default False
        :param glove_vocab_file_path: path of glove vocab file
        """
        if dir:
            self.dir_path = path
            self.file_path = False
        else:
            self.file_path = path
            self.dir_path = False
        if glove_file_path:
            self.glove_file = glove_file_path
            self.glove_vocab_file = glove_vocab_file_path
        else:
            self.glove_file = '/home/sumit/stanford/glove/vector/glove.6B.'+str(dimension)+'d.txt'

        self.save_model = save_model_path

        if dir:
            GWV = GloveWordVector(self.dir_path)
        else:
            GWV = GloveWordVector(self.file_path, dir=False)
        if save_word2vec_path:
            with open(save_word2vec_path, 'rb') as f:
                self.word2vec, self.vocab, self.ivocab = pic.load(f)
        else:
            self.word2vec, self.vocab, self.ivocab = GWV.get_glove_word_vector()

    def get_avg_sentenceVector(self):
        sen2vec = []
        if self.dir_path:
            files = os.walk(self.dir_path).next()[2]
            files = [self.dir_path+file for file in files]
            for index,file in enumerate(files):
                with io.open(file, 'r', encoding='cp437') as f:
                    contents = f.readlines()
                    for l in contents:
                        temp = np.zeros(len(self.word2vec[0]), dtype=float)
                        lexicon = get_lexicon(l)
                        for word in lexicon:
                            temp += self.word2vec[self.vocab[word]]
                        onehotencoder = OneHotEncoder(n_values=len(files))
                        output = onehotencoder.fit_transform(index).toarray()[0]
                        sen2vec.append([temp, output])
        elif self.file_path:
            with io.open(self.file_path, 'r', encoding='cp437') as f:
                contents = f.readlines()
                for l in contents:
                    temp = np.zeros(len(self.word2vec[0]), dtype=float)
                    lexicon = get_lexicon(l)
                    for word in lexicon:
                        temp += self.word2vec[self.vocab[word]]
                    sen2vec.append(temp)
        if self.save_model:
            pic.dump([sen2vec], open(self.save_model+'sen2vec.p', 'wb'))
        return sen2vec

    def get_2D_sentenceVector(self, max = 50):
        sen2vec = []
        if self.dir_path:
            files = os.walk(self.dir_path).next()[2]
            files = [self.dir_path+file for file in files]
            for index, file in enumerate(files):
                with io.open(file, 'r', encoding='cp437') as f:
                    contents = f.readlines()
                    for l in contents:
                        temp = np.zeros([max, len(self.word2vec[0])], dtype=float)
                        count = 0
                        lexicon = get_lexicon(l)
                        for word in lexicon:
                            temp[count] = self.word2vec[self.vocab[word]]
                            count += 1
                        onehotencoder = OneHotEncoder(n_values=len(files))
                        output = onehotencoder.fit_transform(index).toarray()[0]
                        sen2vec.append([temp, output])
        elif self.file_path:
            files = self.file_path
            with io.open(self.file_path, 'r', encoding='cp437') as f:
                contents = f.readlines()
                for l in contents:
                    temp = np.zeros([max, len(self.word2vec[0])], dtype=float)
                    count = 0
                    lexicon = get_lexicon(l)
                    for word in lexicon:
                        temp[count] = self.word2vec[self.vocab[word]]
                        count += 1
                    sen2vec.append(temp)
        if self.save_model:
            pic.dump([sen2vec], open(self.save_model+'sen2vec.p', 'wb'))
        return sen2vec

if __name__ == '__main__':
    Vector_class = GloveSentenceVector('/home/sumit/Desktop/project17/ResumeParser/Data/resume_segments/Level0/',
                                       save_model_path='/home/sumit/Desktop/project17/ResumeParser/Data/resume_segments/Test/')
    sen2vec = Vector_class.get_avg_sentenceVector()
    print len(sen2vec)

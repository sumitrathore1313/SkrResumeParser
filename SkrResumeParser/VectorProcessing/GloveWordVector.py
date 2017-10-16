from DataPreprocessing.Vocab import Vocab
import io
import numpy as np
import cPickle as pic

class GloveWordVector():

    def __init__(self, path, dir=True, dimension=100, glove_file_path=False, save_model_path=False,
                 glove_vocab_file_path=False):
        if dir:
            self.dir_path = path
            self.file_path = False
        else:
            self.file_path = path
            self.dir_path = False
        if glove_file_path:
            self.glove_file = glove_file_path
            self.glove_vocab_file = '/home/sumit/stanford/glove/vector/vocab.txt'
        else:
            self.glove_file = '/home/sumit/stanford/glove/vector/glove.6B.'+str(dimension)+'d.txt'
            self.glove_vocab_file = '/home/sumit/stanford/glove/vector/vocab.txt'
        if dir:
            VC = Vocab(self.dir_path)
        else:
            VC = Vocab(self.file_path, dir=False)
        self.vocablory = VC.get_vocab()
        self.known_vocab, self.unknown_vocab = self.get_known_unknown_vocab()
        self.save_model = save_model_path

    def get_known_unknown_vocab(self):
        f2 = io.open(self.glove_vocab_file, 'rb').read()
        vocab = f2.splitlines()
        known_vocab = []
        unknown_vocab = []
        for word in self.vocablory:
            if word in vocab:
                known_vocab.append(word)
            else:
                unknown_vocab.append(word)
        return known_vocab, unknown_vocab

    def get_known_glove_vector(self):
        vectors = {}
        W = []
        vocab = {}
        ivocab = {}
        f1 = open(self.glove_file, 'rb').read()
        for line in f1.splitlines():
            temp = line.split()
            vectors[temp[0]] = map(float, temp[1:])

        vocab_size = len(self.known_vocab)

        for i in range(len(self.known_vocab)):
            W.append(vectors[self.known_vocab[i]])
            vocab[self.known_vocab[i]] = i
            ivocab[i] = self.known_vocab[i]
        W = np.array(W)
        # normalize each word vector to unit variance
        # print W[0:2], W[-1:-3]
        W_norm = np.zeros(W.shape)
        d = (np.sum(W ** 2, 1) ** (0.5))
        W_norm = (W.T / d).T

        return W_norm, vocab, ivocab

    def get_unknown_vec(self, word2vec, vocab, ivocab):
        old_size = len(vocab)
        word2vec = list(word2vec)
        for i in range(len(self.unknown_vocab)):
            word2vec.append(np.random.uniform(-0.25, 0.25, len(word2vec[0])))
            vocab[self.unknown_vocab[i]] = i + old_size
            ivocab[i + old_size] = self.unknown_vocab[i]
        return word2vec, vocab, ivocab

    def get_glove_word_vector(self):
        Word2vec, vocab, ivocab = self.get_known_glove_vector()
        self.Word2vec, self.vocab, self.ivocab = self.get_unknown_vec(Word2vec, vocab, ivocab)
        if self.save_model:
            pic.dump([self.Word2vec, self.vocab, self.ivocab], open(self.save_model+'word2vec', 'wb'))
        return self.Word2vec, self.vocab, self.ivocab

if __name__ == '__main__':
    wordVector_class = GloveWordVector('/home/sumit/PycharmProjects/ResumeParser/Data/resume_segments/Level0/')
    #print len(wordVector_class.vocablory), len(wordVector_class.unknown_vocab), len(wordVector_class.known_vocab)
    w, v, iv = wordVector_class.get_glove_word_vector()
    print len(w), len(v), len(iv)
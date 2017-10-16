import io
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
import os.path
import re

lemmatizer = WordNetLemmatizer()
tokenizer = RegexpTokenizer(r'\w+')

class Vocab():

    def __init__(self, path, dir = True, save_file = False):
        '''
        This class is used for vocablory operation like generate vocablory from given file or directory
        :param path: path of directory or file
        :param dir: true if diretory is given
        :param save_file: path of fenerate vocablory file
        '''
        if dir:
            self.dir_path = path
            self.file_path = False
        else:
            self.file_path = path
            self.dir_path = False
        self.save_file = save_file

    def get_vocab(self):
        '''
        this funtion generate vocablory
        :return: return vocablory list
        '''
        if self.dir_path:
            files = os.walk(self.dir_path).next()[2]
            files = [self.dir_path+file for file in files]
        elif self.file_path:
            files = [self.file_path]
        lexicon = []
        for file in files:
            with io.open(file, 'r', encoding='cp437') as f:
                contents = f.readlines()
                for l in contents:
                    l = re.sub('[^A-Za-z0-9 ,-./&]+', '', l)
                    all_words = tokenizer.tokenize(l)
                    # all_words = word_tokenize(l)
                    lexicon += list(all_words)
        lexicon = [((lemmatizer.lemmatize(i)).encode('utf8')).lower() for i in lexicon]
        lexicon = sorted(set(lexicon))
        if self.save_file:
            with open(self.save_file, "w") as f:
                for word in lexicon:
                    f.write(word)
                    f.write("\n")

        return lexicon


def get_lexicon(data):
    data = re.sub('[^A-Za-z0-9 ,-/.&]+', '', data)
    all_words = tokenizer.tokenize(data)
    lexicon = list(all_words)
    lexicon = [(lemmatizer.lemmatize(i)).encode('utf8').lower() for i in lexicon]
    return lexicon

if __name__ == '__main__':
    vocab_class = Vocab('/home/sumit/Desktop/project17/ResumeParser/Data/resume_segments/Level0/education.txt', dir=False)
    lexicon = vocab_class.get_vocab()
    print len(lexicon)
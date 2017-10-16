import io
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
import os.path

lemmatizer = WordNetLemmatizer()
tokenizer = RegexpTokenizer(r'\w+')

def get_vocab(file_name):
    '''
    this funtion take file_name and return all vocab in file and also generate vocab file
    :param file_name: vocab file name
    :return:
    '''
    lexicon = []
    with io.open(file_name, 'r', encoding='cp437') as f:
        contents = f.readlines()
        for l in contents:
            all_words = tokenizer.tokenize(l)
            #all_words = word_tokenize(l)
            lexicon += list(all_words)
    lexicon = [((lemmatizer.lemmatize(i)).encode('utf8')).lower() for i in lexicon]
    lexicon = sorted(set(lexicon))
    if not os.path.isfile(file_name+"_vocab"):
        with open(file_name+"_vocab", "w") as f:
            for word in lexicon:
                f.write(word)
                f.write("\n")

    return lexicon

def generate_file(vocab, file_name):
    '''
    this funtion takes vocab list and then generate vocab file
    :param vocab:takes list of vocablory
    :param file_name: generate vocab file
    :return:
    '''
    with open(file_name, 'w') as f:
        for word in vocab:
            f.write(word)
            f.write("\n")
    return 1

def generate_lower_file(filename):
    '''
    this funtion takes file and and convert all lexicon to lower case
    :param filename: file name
    :return:
    '''
    pass
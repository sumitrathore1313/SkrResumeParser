import numpy as np

def get_vector(vector_file = '/home/sumit/stanford-nlp/glove/wiki_GVector/glove.6B.50d.txt', vocab_file =  '/home/sumit/stanford-nlp/glove/wiki_GVector/vocab.txt'):
    vectors = {}
    f2 = open(vocab_file, 'r').read()
    words = f2.splitlines()

    f1 = open(vector_file, 'rb').read()
    for line in f1.splitlines():
        temp = line.split()
        vectors[temp[0]] = map(float, temp[1:])

    vocab_size = len(words)
    vocab = {w: idx for idx, w in enumerate(words)}
    ivocab = {idx: w for idx, w in enumerate(words)}

    vector_dim = len(vectors[ivocab[0]])

    W = np.zeros([vocab_size-1, vector_dim])

    for word, v in vectors.items():
        if word == '<unk>':
            continue
        W[vocab[word]] = v
    # normalize each word vector to unit variance

    W_norm = np.zeros(W.shape)
    d = (np.sum(W ** 2, 1) ** (0.5))
    W_norm = (W.T / d).T

    #evaluate_vectors(W_norm, vocab, ivocab)


def evaluate_vectors(W, vocab, ivocab):
    """Evaluate the trained word vectors on a variety of tasks"""

    filenames = [
        'capital-common-countries.txt', 'capital-world.txt', 'currency.txt',
        'city-in-state.txt', 'family.txt', 'gram1-adjective-to-adverb.txt',
        'gram2-opposite.txt', 'gram3-comparative.txt', 'gram4-superlative.txt',
        'gram5-present-participle.txt', 'gram6-nationality-adjective.txt',
        'gram7-past-tense.txt', 'gram8-plural.txt', 'gram9-plural-verbs.txt',
    ]
    prefix = '/home/sumit/stanford-nlp/glove/eval/question-data/'

    # to avoid memory overflow, could be increased/decreased
    # depending on system and vocab size
    split_size = 100

    correct_sem = 0;  # count correct semantic questions
    correct_syn = 0;  # count correct syntactic questions
    correct_tot = 0  # count correct questions
    count_sem = 0;  # count all semantic questions
    count_syn = 0;  # count all syntactic questions
    count_tot = 0  # count all questions
    full_count = 0  # count all questions, including those with unknown words

    for i in xrange(len(filenames)):
        with open('%s/%s' % (prefix, filenames[i]), 'r') as f:
            full_data = [line.rstrip().split(' ') for line in f]
            full_count += len(full_data)
            data = [x for x in full_data if all(word in vocab for word in x)]

        indices = np.array([[vocab[word] for word in row] for row in data])
        ind1, ind2, ind3, ind4 = indices.T

        predictions = np.zeros((len(indices),))
        num_iter = int(np.ceil(len(indices) / float(split_size)))
        for j in xrange(num_iter):
            subset = np.arange(j * split_size, min((j + 1) * split_size, len(ind1)))

            pred_vec = (W[ind2[subset], :] - W[ind1[subset], :]
                        + W[ind3[subset], :])
            # cosine similarity if input W has been normalized
            dist = np.dot(W, pred_vec.T)

            for k in xrange(len(subset)):
                dist[ind1[subset[k]], k] = -np.Inf
                dist[ind2[subset[k]], k] = -np.Inf
                dist[ind3[subset[k]], k] = -np.Inf

            # predicted word index
            predictions[subset] = np.argmax(dist, 0).flatten()

        val = (ind4 == predictions)  # correct predictions
        count_tot = count_tot + len(ind1)
        correct_tot = correct_tot + sum(val)
        if i < 5:
            count_sem = count_sem + len(ind1)
            correct_sem = correct_sem + sum(val)
        else:
            count_syn = count_syn + len(ind1)
            correct_syn = correct_syn + sum(val)

        print("%s:" % filenames[i])
        print('ACCURACY TOP1: %.2f%% (%d/%d)' %
              (np.mean(val) * 100, np.sum(val), len(val)))

    print('Questions seen/total: %.2f%% (%d/%d)' %
          (100 * count_tot / float(full_count), count_tot, full_count))
    print('Semantic accuracy: %.2f%%  (%i/%i)' %
          (100 * correct_sem / float(count_sem), correct_sem, count_sem))
    print('Syntactic accuracy: %.2f%%  (%i/%i)' %
          (100 * correct_syn / float(count_syn), correct_syn, count_syn))
    print('Total accuracy: %.2f%%  (%i/%i)' % (100 * correct_tot / float(count_tot), correct_tot, count_tot))


def distance(W, vocab, ivocab, input_term):
    for idx, term in enumerate(input_term.split(' ')):
        if term in vocab:
            print('Word: %s  Position in vocabulary: %i' % (term, vocab[term]))
            if idx == 0:
                vec_result = np.copy(W[vocab[term], :])
            else:
                vec_result += W[vocab[term], :]
        else:
            print('Word: %s  Out of dictionary!\n' % term)
            return

    vec_norm = np.zeros(vec_result.shape)
    d = (np.sum(vec_result ** 2, ) ** (0.5))
    vec_norm = (vec_result.T / d).T

    dist = np.dot(W, vec_norm.T)

    for term in input_term.split(' '):
        index = vocab[term]
        dist[index] = -np.Inf

    a = np.argsort(-dist)[:N]

    print("\n                               Word       Cosine distance\n")
    print("---------------------------------------------------------\n")
    for x in a:
        print("%35s\t\t%f\n" % (ivocab[x], dist[x]))


if __name__ == "__main__":
    N = 100;  # number of closest words that will be shown
    W, vocab, ivocab = get_vector()
    while True:
        input_term = raw_input("\nEnter word or sentence (EXIT to break): ")
        if input_term == 'EXIT':
            break
        else:
            distance(W, vocab, ivocab, input_term)



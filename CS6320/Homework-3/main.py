import re
import argparse
from pos import POSTagger
from hmm import Viterbi


TAGS = ['NNP', 'MD', 'VB', 'JJ', 'NN', 'RB', 'DT']


WORDS = ['Janet', 'will', 'back', 'the', 'bill']


DELTA = [[0.2767, 0.0006, 0.0031, 0.0453, 0.0449, 0.0510, 0.2026],
         [0.3777, 0.0110, 0.0009, 0.0084, 0.0584, 0.0090, 0.0025],
         [0.0008, 0.0002, 0.7968, 0.0005, 0.0008, 0.1698, 0.0041],
         [0.0322, 0.0005, 0.0050, 0.0837, 0.0615, 0.0514, 0.2231],
         [0.0366, 0.0004, 0.0001, 0.0733, 0.4509, 0.0036, 0.0036],
         [0.0096, 0.0176, 0.0014, 0.0086, 0.1216, 0.0177, 0.0068],
         [0.0068, 0.0102, 0.1011, 0.1012, 0.0120, 0.0728, 0.0479],
         [0.1147, 0.0021, 0.0002, 0.2157, 0.4744, 0.0102, 0.0017]]


LIKELIHOOD = [[0.000032, 0, 0, 0.000048, 0],
              [0, 0.308431, 0, 0, 0],
              [0, 0.000028, 0.000672, 0, 0.000028],
              [0, 0, 0.000340, 0, 0],
              [0, 0.000200, 0.000223, 0, 0.002337],
              [0, 0, 0.010446, 0, 0],
              [0,0, 0, 0.506099, 0]]


def preprocess(sentence, transform):
    """Preprocesses sentence based on recommendations in assignment.

    Arguments:
        transform (bool):
            If True, input sentence is handled as a test sequence.
            If False, input sentence is handled as a sentence in
            training corpus.

    Returns:
        tokens (list):
            List of processed tokens in sentence.
    """
    sentence = sentence.rstrip('\n').rstrip()

    if not transform:
        start, end = ['<s>_<s>'], ['</s>_</s>']
        tokens = start + re.split('\s', sentence) + end
    else:
        tokens = re.split('\s', sentence)
    return tokens


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='CS6320: Homework 3')
    parser.add_argument('--run', dest='run', type=str,
                        choices=['pos', 'hmm'],
                        required=True, help='Identifier program to run, choices are:\
                        (a) pos: Parts-of-Speech Tagger, Q1. \
                        (b) hmm: Hidden Markov Model, Q2.')
    parser.add_argument('--debug', dest='debug', action='store_true',
                        help='To debug output of :func: `transform` in POSTagger,\
                        pass this flag.')
    args = parser.parse_args()


    if args.run == 'pos':
        with open('train.txt', 'r') as input_file:
            sentences = input_file.readlines()

        sentences = [preprocess(sentence, transform=False) for sentence in sentences]
        
        tagger = POSTagger()

        tagger.fit(sentences)
#       sentence = 'Brainpower has the seal .'
        sentence = input('Enter sentence to compute POS tags: ')
        tagger.transform(preprocess(sentence, transform=True),
                         debug=args.debug)

    elif args.run == 'hmm':
        model = Viterbi(WORDS, TAGS, DELTA, LIKELIHOOD)
        sentence = input('Enter sentence to compute POS tags: ')
        model.transform(sentence)
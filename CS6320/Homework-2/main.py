import re
import argparse
from ngram import Bigram


def preprocess(sentence):
    """Preprocesses sentence based on recommendations in assignment.
    """
    sentence = sentence.rstrip('\n').rstrip()
    tokens = re.split('\s', sentence)
    tokens = [token.split('_')[0].lower() for token in tokens]
    return tokens


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='CS6320: Homework 2')
    parser.add_argument('--smoothing', dest='smoothing', type=str,
                        choices=['laplacian', 'good-turing'],
                        help='Normalizing technique. Options are \'laplacian\' \
                        and \'good-turing\'. If argument is not passed, no smoothing \
                        is done.')
    parser.add_argument('--N', dest='N', type=int, default=20,
                        help='Top N word/bigram frequencies are printed.')
    parser.add_argument('--transform', dest='transform', action='store_true',
                        help='If passed, transforms sentence in \'test.txt\' according to \
                        the trained N-gram model.\n \
                        NOTE: Test sentence should follow WORD_POS format, as in \'train.txt\'.')
    parser.add_argument('--debug', dest='debug', action='store_true',
    	                help='To debug output of :func: `transform`, pass this flag.')

    args = parser.parse_args()

    with open('train.txt', 'r') as input_file:
        sentences = input_file.readlines()

    sent_tokens = [preprocess(sentence) for sentence in sentences]
    
    model = Bigram(smoothing=args.smoothing)
    model.fit(sent_tokens)

    sorted_unigram_counts = dict(sorted(model.unigram_counts.items(),
                                         key=lambda item: item[1],
                                         reverse=True))
    sorted_bigram_counts = dict(sorted(model.bigram_counts.items(),
                                       key=lambda item: item[1],
                                       reverse=True))
    if not args.transform:
        print(f"Showing Top-{args.N} word frequencies:")
        print(dict(zip(list(sorted_unigram_counts.keys())[:args.N],
                       list(sorted_unigram_counts.values())[:args.N])))
        print('')
        print(f"Showing Top-{args.N} bigram frequencies:")
        print(dict(zip(list(sorted_bigram_counts.keys())[:args.N],
                       list(sorted_bigram_counts.values())[:args.N])))

    if args.transform:
        with open('test.txt', 'r') as input_file:
            sentence = input_file.readline()
        test_sent_tokens = preprocess(sentence)
        probability = model.transform(test_sent_tokens, args.debug)
        print(f'=> Bigram probability of sentence = {probability}')

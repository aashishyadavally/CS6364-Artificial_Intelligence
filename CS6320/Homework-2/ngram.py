import math
from collections import Counter


class Bigram:
    """Fits a bigram model for training data set, and computes
    bigram probability for a given sentence.

    Parameters:
        smoothing (str or None):
            If None, no smoothing is applied.
            If 'laplacian', add-one smoothing is applied.
            If 'good-turing', good turing discounting is applied.           
        unigram_counts (dict):
            Dictionary of unigrams in the training set, and their
            corresponding counts.
        bigram_counts (dict):
            Dictionary of bigrams in the training set, and their
            corresponding counts.
    """
    def __init__(self, smoothing=None):
        """Initializes :class: ``Bigram``.

        Arguments:
            smoothing (str or None):
                If None, no smoothing is applied.
                If 'laplacian', add-one smoothing is applied.
                If 'good-turing', good turing discounting is applied.
        """
        self.unigram_counts = {}
        self.bigram_counts = {}
        self.smoothing = smoothing

    def _get_tokens_counts(self):
        tokens = self.bigram_counts
        tokens_counts = list(tokens.values())
        return tokens_counts

    def _get_Nc(self, count):
        tokens_counts = self._get_tokens_counts()
        if tokens_counts.count(count) == 0:
            Nc = 1
        else:
            Nc = tokens_counts.count(count)
        return Nc

    def _get_Nc_plus_1(self, count):
        tokens_counts = self._get_tokens_counts()
        Nc_plus_1 = tokens_counts.count(count + 1)
        return Nc_plus_1

    def _get_N(self):
        tokens_counts = self._get_tokens_counts()
        return sum(tokens_counts)

    def _normalize_bigram(self, count):
        if self.smoothing is None:
            return count
        elif self.smoothing == 'laplacian':
            return count + 1
        elif self.smoothing == 'good-turing':
            c_star = (count + 1) * self._get_Nc_plus_1(count) \
                                   / self._get_Nc(count)
            prob_gt = c_star / self._get_N()
            return prob_gt

    def _normalize_previous(self, count):
        if self.smoothing is None:
            return count
        elif self.smoothing == 'laplacian':
            return count + len(self.unigram_counts)
        elif self.smoothing == 'good-turing':
            return 1

    def fit(self, sentence_tokens):
        """Fit bigram model.

        Arguments:
            sentence_tokens (list):
                List of sentences, represented as a list of tokens.
        """
        for each in sentence_tokens:
            unigram_counts = dict(Counter(each))
            for x in unigram_counts:
                if x in self.unigram_counts:
                    self.unigram_counts[x] += unigram_counts[x]
                else:
                    self.unigram_counts[x] = unigram_counts[x]

            bigrams = [(each[i - 1], each[i]) for i in range(1, len(each))]
            bigram_counts = dict(Counter(bigrams))

            for x in bigram_counts:
                if x in self.bigram_counts:
                    self.bigram_counts[x] += bigram_counts[x]
                else:
                    self.bigram_counts[x] = bigram_counts[x]
        return self

    def transform(self, sentence_tokens, debug=False):
        """Bigram probabilities computed for a sentence, represented
        as a list of tokens.

        Arguments:
            sentence_tokens (list):
                List of tokens corresponding to a sentence.

        Returns:
            prob (float):
                Bigram probability with/without smoothing.
        """
        bigrams = [(sentence_tokens[i - 1], sentence_tokens[i]) \
                   for i in range(1, len(sentence_tokens))]
        prob = self.unigram_counts[sentence_tokens[0]] \
                    / sum(list(self.unigram_counts.values()))

        debug_string = f'P({sentence_tokens[0]})'
        debug_op_string = f'{prob}'

        for bigram in bigrams:
            if bigram not in self.bigram_counts:
                numerator = self._normalize_bigram(0)
            else:
                numerator = self._normalize_bigram(self.bigram_counts[bigram])
            denominator =  self._normalize_previous(self.unigram_counts[bigram[0]])
            bigram_prob = numerator / denominator
            prob = prob * bigram_prob

            debug_string += f' * P({bigram[1]} | {bigram[0]})'
            debug_op_string += f' * {bigram_prob}'

        if debug:
            print(f"Sentence: {' '.join(sentence_tokens)}")
            print(f'Bigram probability of sentence = {debug_string}')
            print(f'=> Bigram probability of sentence = {debug_op_string}')
        return prob

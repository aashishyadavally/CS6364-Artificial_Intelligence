"""
Implementation of Parts-of-speech Tagger using a Bigram Model.

Here, no smoothing is performed, i.e. if a word in the test sequence
is not present in the vocabulary, then no tag-sequence is returned.
"""


from itertools import product
from collections import Counter


class POSTagger:
    """Parts of Speech Tagger using a Bigram Model without smoothing.

    Parameters:
        word_tags (dict):
            Maps a combination of a word and its POS tag to their
            respective count in the corpus.
        tag_unigrams (dict):
            Maps each POS tag in the corpus with its resective count.
        tag_bigrams (dict):
            Maps each combination of two POS tags in the corpus with
            its resective count.
        vocabulary_tag_mapper (None or dict):
            Maps each word in the corpus with all the POS tags it was
            used as.
    """
    def __init__(self):
        """Initializes :class: ``POSTagger``.
        """
        self.word_tags = {}
        self.tag_unigrams = {}
        self.tag_bigrams = {}


    def _map_words_to_tags(self, sentence_tokens):
        """
        """
        vocabulary_tag_mapper = {}

        for sent in sentence_tokens:
            for each in sent:
                word, tag = each.split('_')
                if word in vocabulary_tag_mapper:
                    if tag not in vocabulary_tag_mapper[word]:
                        vocabulary_tag_mapper[word].add(tag)
                else:
                    vocabulary_tag_mapper[word] = set([tag])

        for word in vocabulary_tag_mapper:
            tags = list(vocabulary_tag_mapper[word])
            vocabulary_tag_mapper[word] = tags
        return vocabulary_tag_mapper


    def _get_tag_combinations(self, words):
        """Computes all possible combinations of POS tags for a given
        sentence.

        Arguments:
            words (list):
                List of tokens in a sentence.

        Returns:
            tag_combs (itertools.product)
                All possible combinations of POS tags corresponding to
                each word in a sentence.
        """
        tag_lists = [self.vocabulary_tag_mapper[word] for word in words]
        tag_combs = product(*tag_lists)
        return tag_combs
                

    def fit(self, sentence_tokens):
        """Fit parts of speech tagger model on the sentences.

        Arguments:
            sentence_tokens (list of lists):
                List of tokens in each sentence in corpus.
        """
        self.vocabulary_tag_mapper = self._map_words_to_tags(sentence_tokens)

        for sent in sentence_tokens:
            for each in sent:
                word, tag = each.split('_')
                if (word, tag) in self.word_tags:
                    count = self.word_tags[(word, tag)]
                    self.word_tags[(word, tag)] = count + 1
                else:
                    self.word_tags[(word, tag)] = 1

        tag_tokens = []
        for sent in sentence_tokens:
            tag_tokens.append([each.split('_')[1] for each in sent])

        for each in tag_tokens:
            unigram_counts = dict(Counter(each))

            for ug in unigram_counts:
                if ug in self.tag_unigrams:
                    self.tag_unigrams[ug] += unigram_counts[ug]
                else:
                    self.tag_unigrams[ug] = unigram_counts[ug]

            bigrams = [(each[i - 1], each[i]) for i in range(1, len(each))]
            bigram_counts = dict(Counter(bigrams))

            for bg in bigram_counts:
                if bg in self.tag_bigrams:
                    self.tag_bigrams[bg] += bigram_counts[bg]
                else:
                    self.tag_bigrams[bg] = bigram_counts[bg]
        return self


    def transform(self, sentence_tokens, debug):
        """Parts of speech tags are computer for a sentence, represented
        as a list of tokens.

        If ``debug`` argument is passed, steps to compute the parts of
        speech tags are presented.

        Arguments:
            sentence_tokens (list):
                List of tokens in a sentence.
            debug (bool):
                Debugging flag

        Returns:
            argmax_tags (list):
                Sequence of tags for the sentence.
            argmax_prob (float):
                Probability of sequence of tags.
        """
        for word in sentence_tokens:
            if word not in self.vocabulary_tag_mapper:
                print('Input sentence contains out-of-vocabulary words.')
                print('Probability of tags = 0')
                return

        tag_combs = list(self._get_tag_combinations(sentence_tokens))
        probs = {}

        for index, tags in enumerate(tag_combs):
            prob = 1
            tags = ['<s>'] + list(tags) + ['</s>']

            for i, word in enumerate(sentence_tokens):
                prob *= (self.word_tags.get((word, tags[i + 1]), 0) / self.tag_unigrams[tags[i + 1]]) * \
                        (self.tag_bigrams.get((tags[i], tags[i + 1]), 0) / self.tag_unigrams[tags[i]])
            prob *= self.tag_bigrams.get((tags[-2], tags[-1]), 0) / self.tag_unigrams[tags[-2]]
            probs[str(index)] = prob

        argmax_prob = max(probs.values())
        max_prob_tags_index = int(max(probs, key = lambda x: probs[x]))
        argmax_tags = tag_combs[max_prob_tags_index]

        print('')
        print(f"Sentence is: {' '.join(sentence_tokens)}")
        print(f'Corresponding POS tags are: {argmax_tags}')

        if debug:
            prod_notation, prod = '', ''
            tags = ['<s>'] + list(argmax_tags) + ['</s>']

            for i, word in enumerate(sentence_tokens):
                prod_notation += f'P({word} | {tags[i + 1]}) * P({tags[i + 1]} | {tags[i]}) * \n'
                prod += f'{self.word_tags.get((word, tags[i + 1]), 0) / self.tag_unigrams[tags[i + 1]]} * '\
                        f'{self.tag_bigrams.get((tags[i], tags[i + 1]), 0) / self.tag_unigrams[tags[i]]} * \n'

            prod_notation += f'P({tags[-1]} | {tags[-2]})'
            prod += f'{self.tag_bigrams.get((tags[-2], tags[-1]), 0) / self.tag_unigrams[tags[-2]]}'

            print('')
            print('Steps:')
            print('------\n')
            print(prod_notation)
            print(f'= {prod}')
            print('')

        print(f'Probability of tags = {argmax_prob}')
        
        return argmax_tags, argmax_prob
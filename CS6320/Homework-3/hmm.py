"""
Implementation of Hidden Markov Models (HMMs) using Viterbi Algorithm
to decode the Parts of Speech tags for a given sentence.

Though the variable names in the implementation indicate dependency
on NLP ideas, can be extended to any HMM problem. 

Tested with the famous EISNER-ICECREAMS Hidden Markov Model example.

    TAGS = ['H','C']

    WORDS = ['1', '2', '3']

    DELTA = [[0.8, 0.2],
             [0.7, 0.3],
             [0.4, 0.6]]

    LIKELIHOOD = [[0.2, 0.4, 0.4],
                  [0.5, 0.4, 0.1]]
"""


class Viterbi:
    """Viterbi algorithm in Hidden Markov Moels to decode 
    possible sequence of POS tags for a sentence.

    Parameters:
        vocabulary (list):
            List of words in corpus.
        pos_tags (list):
            List of POS tags in corpus.
        delta (list of lists):
            State Transition matrix.
        obs (list of lists):
            Observation Likelihood matrix.
    """
    def __init__(self, vocabulary, pos_tags, delta, obs):
        """Initializes :class: ``Viterbi``.

        Arguments:
            vocabulary (list):
                List of words in corpus.
            pos_tags (list):
                List of POS tags in corpus.
            delta (list of lists):
                State Transition matrix.
            obs (list of lists):
                Observation Likelihood matrix.
        """
        self.vocabulary = vocabulary
        self.pos_tags = pos_tags
        self.delta = delta
        self.obs = obs


    def _initialize(self, first):
        """Initialization Step in Viterbi Algorithm

        Arguments:
            first (str):
                First word in sequence.

        Returns:
            start_probs (list):
                List of probabilities of each POS tag to be at the
                beginning of a sentence.
        """
        word_index = self.vocabulary.index(first)
        start_tag_probs = self.delta[0]

        start_probs = []
        for i, tag in enumerate(self.pos_tags):
            # P(tag | start) * P(word | tag)
            p = start_tag_probs[i] * self.obs[i][word_index]
            start_probs.append(p)

        return start_probs


    def _compute_forward_path_prob(self, word, probs_t_minus_1):
        """Recursive step to compute the probability of being in a
        particular state after seeing the first ``t`` observations.

        Arguments:
            word (str):
                Word in input sequence.
            probs_t_minus_1 (list of lists):
                Probability of states in t-1 level of HMM.

        Returns:
            probs_t (list of lists):
                Probability of states in t level of HMM.
            backpointer_t (list of lists):
                Array containing argmax indices at each level
                in HMM.
        """
        word_index = self.vocabulary.index(word)

        probs_t, backpointer_t = [], []
        for i in range(len(self.pos_tags)):
            joint_probs = []
            for j in range(len(self.pos_tags)):
                # P(tag | tag_t_minus_1) * P(word | tag)
                p = self.delta[j + 1][i] * self.obs[i][word_index]
                joint_probs.append(p)

            _joint_probs = [a * b for a, b in zip(probs_t_minus_1, joint_probs)]
            probs_t.append(max(_joint_probs))
            backpointer_t.append(_joint_probs.index(max(_joint_probs)))
        return probs_t, backpointer_t


    def _decode_sequence(self, probs_tn, backpointer):
        """Uses backpointer containing argmax indices for each level
        in the HMM to compute the most probable sequence of POS tags.

        Arguments:
            probs_tn (list):
                List of probabilities of tags in final level in HMM.
            backpointer (list):
                List of argmax indices for each level in HMM.

        Returns:
            sequence (list):
                List of POS tags corresponding to input sequence.
        """
        n = len(backpointer), 
        max_probs_t_ix = probs_tn.index(max(probs_tn)) 
        sequence_rev = [self.pos_tags[max_probs_t_ix]]

        for indices in reversed(backpointer):
            max_probs_t_ix = indices[max_probs_t_ix]
            tag_t = self.pos_tags[max_probs_t_ix]
            sequence_rev.append(tag_t)


        sequence = list(reversed(sequence_rev))
        return sequence


    def transform(self, sentence):
        """Given the HMM model, computes the most probable sequence
        of POS tags for a sentence using the Viterbi algorithm.

        Arguments:
            sentence (str):
                Input sentence for which POS tags need to be computed.
        """
        tokens = sentence.split(' ')

        for token in tokens:
            if token not in self.vocabulary:
                return 0

        start_probs = self._initialize(tokens[0])
        probs, backpointer = [], []

        probs_t_minus_1 = start_probs
        for word in tokens[1:]:
            probs_t, backpointer_t = self._compute_forward_path_prob(word, probs_t_minus_1)
            probs.append(probs_t)
            backpointer.append(backpointer_t)
            probs_t_minus_1 = probs_t

        sequence = self._decode_sequence(probs[-1], backpointer)

        print(f'Sentence is: {sentence}')
        print(f'POS Tags are: {sequence}')
        print(f'Probability = {max(probs[-1])}')

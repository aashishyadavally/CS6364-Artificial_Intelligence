GETTING STARTED:
===============
This section describes the preqrequisites, and contains instructions, to get the project up and running.

> Prerequisites
  -------------
  Python >= 3.6

> Usage
  -----
    The user can get a description of the options by using the command: $ python main.py --help

    User Options:

    -   --run
        Indicates which program to run, choices are:
        (a) pos: Parts of Speech Tagger (Question 1)
        (b) hmm: Hidden Markov Model (Question 2)
    -   --debug
        Flag if passed, sentence transformation with fit model is debugged by printing corresponding probabilites.
        Valid argument for Parts of Speech Tagger.

> Points to Note
  --------------

    (a) The test sentences are not subject to smoothing. Thus, if any out-of-vocabulary (oov) words are entered,
    the probability of tag sequence for the same would be 0.0

> Sample Run Commands
  -------------------
    $ python main.py --run pos

    $ python main.py --run pos --debug

    $ python main.py --run hmm

> Sample Input/Output
  -------------------
  1. Parts of Speech Tagger:
      a. Input:
         ------
         Brainpower has the seal .

         Output:
         -------
         Corresponding POS tags are: ('NNP', 'VBZ', 'DT', 'NN', '.')
         Probability of tags = 2.9172072937962105e-13

  2. Hidden Markov Model:
      a. Input:
         ------
         Janet will back the bill

         Output:
         -------
         POS Tags are: ['NNP', 'MD', 'VB', 'DT', 'NN']
         Probability = 2.0135707102213855e-15

      b. Input:
         ------
         will Janet back the bill

         Output:
         -------
         POS Tags are: ['MD', 'NNP', 'RB', 'DT', 'NN']
         Probability = 1.197060647537461e-20

      c. Input:
         ------
         back the bill Janet will

         Output:
         -------
         POS Tags are: ['RB', 'DT', 'NN', 'NNP', 'MD']
         Probability = 1.492335607263368e-17
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

    -   --smoothing
    	  Normalizing technique. Options are:
        (a) laplacian: Add-one smoothing
        (b) good-turing: Good Turing discounting
        If flag is not passed, smoothing is not applied.
    -   --N
        Top N word/bigram frequencies are printed.
    -   --transform
        Flag if passed, transforms sentence in 'test.txt' according to the trained N-gram model.
    -   --debug
        Flag if passed, sentence transformation with fit model is debugged by printing corresponding probabilites.

> Points to Note
  --------------

    (a) Sentence to be transformed should be placed in 'test.txt' file.
    (b) Test sentence should conform to WORD_POS format in 'train.txt' file.
    (c) Not passing the '--smoothing' flag does not apply any smoothing technique.
    (d) Not passing the '--transform' flag prints top-N unigram/bigram counts without smoothing.
        This is irrespective of '--smoothing' flag.

> Sample Run Commands
  -------------------
    $ python main.py 

    $ python main.py --smoothing laplacian --transform

from functools import partial
from utils.misc_data import getRandomSentence, getRandomSentiment
import random

# UTILS
def generateBalanced( generator, scoring_rule, fraction_positive, num_train, num_test ):
    """
    Given a generator and a boolean scoring function
    generate a balanced dataset of size n with fraction_positive
    of the data being positive examples.
    and split it into balanced train and test sets
    """

    # Ensure we have enough of each type
    n = num_train + num_test

    positive_needed = int(n * fraction_positive)
    negative_needed = n - positive_needed

    negative = []
    positive = []

    gen_obj = generator()
    while len(positive) < positive_needed or len(negative) < negative_needed:
        sample = next(gen_obj)
        yes = scoring_rule(sample)

        if yes and len(positive) < positive_needed:
            positive.append(sample)
        elif not yes and len(negative) < negative_needed:
            negative.append(sample)

    pos_train = int(num_train * fraction_positive)
    neg_train = num_train - pos_train
    
    negative_train, negative_test = negative[:neg_train], negative[neg_train:]
    positive_train, positive_test = positive[:pos_train], positive[pos_train:]

    all_train = negative_train + positive_train
    all_test = negative_test + positive_test
    random.shuffle(all_train)
    random.shuffle(all_test)

    return all_train, all_test

# TEXT
import re

def containsSubstringsScoringRule(sentence, substr, n, full_word=True):
    """
    Checks if a sentence contains a given substring, considering full_word flag.

    Args:
    sentence (str): The sentence to check.
    substr (str): The substring to look for in the sentence.
    n (int): The minimum number of times substr should appear in the sentence.

    Returns:
    bool: True if the substr is present in the sentence as per the specified conditions, False otherwise.
    """
    if full_word:
        # Using regex to find matches of substr bordered by non-alphanumeric characters
        pattern = r'([^a-zA-Z])' + re.escape(substr) + r'([^a-zA-Z0-9])'
        matches = re.findall(pattern, sentence)
        return len(matches) >= n
    else:
        # Counting the occurrence of substr in sentence
        return sentence.count(substr) >= n


def word_substr(word, fraction_positive):
    desc = f"True iff the input contains the substring '{word}'"
    name = f"has_{word}"

    scoring_rule = partial(containsSubstringsScoringRule, substr=word, n=1)
    sample_generator = partial( generateBalanced, generator=getRandomSentence, scoring_rule=scoring_rule, fraction_positive=fraction_positive )

    return desc, name, scoring_rule, sample_generator

def sentiment( positive=True, fraction_positive = 0.5 ):
    desc = f"True iff the text sentiment is {'positive' if positive else 'negative'}"
    name = f"sentiment_{'positive' if positive else 'negative'}"

    scoring_rule = lambda x: x.label
    sample_generator = partial( generateBalanced, generator=getRandomSentiment, scoring_rule=scoring_rule, fraction_positive=fraction_positive )

    return desc, name, scoring_rule, sample_generator

def colorNonContrastive( fraction_positive = 0.5 ):
    with open( "./colors.txt" ) as f:
        colors = [line.strip() for line in f.readlines()]
    
    def scoring_rule(sentence):
        for color in colors:
            color = color.lower()
            pattern = r'([^a-zA-Z])' + re.escape(color) + r'([^a-zA-Z0-9])'
            matches = re.findall(pattern, sentence)
            if len(matches) > 0:
                return True
        return False
    
    desc = "True iff the input contains a color (non-contrastive)"
    name = "color_non_contrastive"

    sample_generator = partial( generateBalanced, generator=getRandomSentence, scoring_rule=scoring_rule, fraction_positive=fraction_positive )

    return desc, name, scoring_rule, sample_generator


def flowerNonContrastive( fraction_positive = 0.5 ):
    return word_substr('flower', fraction_positive)

def exquisiteNonContrastive( fraction_positive = 0.5 ):
    return word_substr('exquisite', fraction_positive)

def hasHyphenNonContrastive( fraction_positive = 0.5 ):
    return word_substr('-', fraction_positive)

# CHESS
import chess.pgn

def readPgnFile(file_path):
    with open(file_path) as pgn:
        while True:
            game = chess.pgn.read_game(pgn)
            if game is None:
                break
            print(game.headers["Event"], game.headers["White"], game.headers["Black"])
            # Do something with the game

def chessGameGenerator( max_len=100 ): #n, scoring_rule, fraction_positive = 0.5, max_len=250 ):
    fp = "./lichess_db_standard_rated_2013-01.pgn"

    # Ensure we have enough of each type
    # positive_needed = int(n * fraction_positive)
    # negative_needed = n - positive_needed

    # positives = []
    # negatives = []

    with open(fp) as pgn:
        # while len(positives) < positive_needed or len(negatives) < negative_needed:
        while True:
            game = chess.pgn.read_game(pgn)
            game_str = str(game).split("\n")[-1]
            if len(game_str) > max_len:
                continue
            yield game_str

    #         yes = scoring_rule(game_str)

    #         if yes and len(positives) < positive_needed:
    #             positives.append(game_str)
    #         elif not yes and len(negatives) < negative_needed:
    #             negatives.append(game_str)

    # all_samples = positives + negatives
    # random.shuffle(all_samples)

    # return all_samples

def whiteChessGamesNonContrastive( fraction_positive = 0.5 ):
    desc = "True iff white won the game (non-contrastive)"
    name = "white_chess_non_contrastive"

    scoring_rule = lambda x: '1-0' in str(x)
    sample_generator = partial( generateBalanced, generator=chessGameGenerator, scoring_rule=scoring_rule, fraction_positive=fraction_positive )
    # sample_generator = partial(chessGameGenerator, scoring_rule=scoring_rule, fraction_positive=fraction_positive)

    return desc, name, scoring_rule, sample_generator

def kingChessGamesNonContrastive( fraction_positive = 0.5 ):
    desc = "True iff either king captured a piece (non-contrastive)"
    name = "king_chess_non_contrastive"

    scoring_rule = lambda x: 'Kx' in str(x)
    sample_generator = partial( generateBalanced, generator=chessGameGenerator, scoring_rule=scoring_rule, fraction_positive=fraction_positive )
    # sample_generator = partial(chessGameGenerator, scoring_rule=scoring_rule, fraction_positive=fraction_positive)

    return desc, name, scoring_rule, sample_generator

# NUMBERS
def numberGenerator(num_digits=4, space_separated=True):
    while True:
        r = random.randint(10**num_digits, 10**(num_digits+1))
        if space_separated:
            yield " ".join(list(str(r)))
        else:
            yield str(r)

def multipleSevens( fraction_positive = 0.5, num_digits=4 ):
    desc = "True iff the input contains multiple 7s"
    name = f"multiple_sevens_{num_digits}"

    scoring_rule = lambda x: x.count('7') > 1
    def gen():
        return numberGenerator(num_digits=num_digits)
    
    sample_generator = partial( generateBalanced, generator=gen, scoring_rule=scoring_rule, fraction_positive=fraction_positive )

    return desc, name, scoring_rule, sample_generator

def multipleZeros( fraction_positive = 0.5, num_digits=4 ):
    desc = "True iff the input contains multiple 0s"
    name = f"multiple_zeros_{num_digits}"

    scoring_rule = lambda x: x.count('0') > 1
    def gen():
        return numberGenerator(num_digits=num_digits)
    
    sample_generator = partial( generateBalanced, generator=gen, scoring_rule=scoring_rule, fraction_positive=fraction_positive )

    return desc, name, scoring_rule, sample_generator

def isNonDescending( fraction_positive = 0.5, num_digits=4 ):
    desc = "True iff the input's digits are non-descending"
    name = f"non_descending_{num_digits}"

    scoring_rule = lambda x: sorted(x.split(" ")) == x.split(" ")
    def gen():
        return numberGenerator(num_digits=num_digits)
    
    sample_generator = partial( generateBalanced, generator=gen, scoring_rule=scoring_rule, fraction_positive=fraction_positive )

    return desc, name, scoring_rule, sample_generator

from sympy import isprime
def isPrime( fraction_positive = 0.5, num_digits=4 ):
    desc = "True iff the input's digits are non-descending"
    name = f"non_descending_{num_digits}"

    scoring_rule = lambda x: isprime(int(x))
    def gen():
        return numberGenerator(num_digits=num_digits, space_separated=False)
    
    sample_generator = partial( generateBalanced, generator=gen, scoring_rule=scoring_rule, fraction_positive=fraction_positive )

    return desc, name, scoring_rule, sample_generator
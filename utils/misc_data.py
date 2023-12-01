import nltk
from nltk.corpus import gutenberg
import random

# Download the Gutenberg corpus
nltk.download('gutenberg')
nltk.download('punkt')

def genVaryingSentences(n, filter_fn=lambda x: True, shuffle=True):
    # Load sentences from a text in the Gutenberg corpus
    sentences = nltk.sent_tokenize(" ".join(gutenberg.raw().split()))
    if shuffle:
        random.shuffle(sentences)

    generated_sentences = []
    for sentence in sentences:
        if filter_fn(sentence):
            generated_sentences.append(sentence)
            if len(generated_sentences) >= n:
                break

    return generated_sentences

def getRandomSentence(shuffle=True):
   # Load sentences from a text in the Gutenberg corpus
    sentences = nltk.sent_tokenize(" ".join(gutenberg.raw().split()))
    if shuffle:
        random.shuffle(sentences)

    for sentence in sentences:
        yield sentence

from datasets import load_dataset

class SentimentObj:
    def __init__(self, text, label):
        self.text = text
        self.label = label

    def __str__(self) -> str:
        return self.text
    
def getRandomSentiment(shuffle=True):
    # Load the IMDB dataset
    data = [(example["text"], example["label"]) for example in load_dataset("imdb", split="train")]
    if shuffle:
        random.shuffle(data)

    for s, l in data:
        l = l == 1
        yield SentimentObj(s, l)


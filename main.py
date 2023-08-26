'''
Command line Python game based on the web word puzzle game Contexto.
The goal of the game is to guess the correct word. Each guess will return a similarity score to the answer word.
Guess the correct word in the least attempts based on the similarity scores returned by your guesses.

@author Gabriel Hooks
@date 2023-08-26
'''

'''
FEATURES TO INCLUDE:

- Difficulty settings:
  - Select one or more word categories (nouns, adjectives, verbs, etc.).
  - Select how many words from each category.
  - Preset difficulties (easy, medium, hard) which have selected categories and word counts.
  - Hints?

- Colored text
- Pretty printing and screen clearing
- Print already guessed words and scores each turn
- Forfeit
- High score
- Daily word
'''


import colorama
import re
import json
from gensim.models import KeyedVectors
from sklearn.metrics.pairwise import cosine_similarity

# Words from Oxford dictionary
eng_dict = []

def loadEngDictionary():
    words = []
    words_new = []

    # Open and read dictionary.json
    with open('data/dictionary.json', encoding='utf-8') as eng_dict_f:
        try:
            words = list(json.load(eng_dict_f).keys())
            print("Loaded and parsed dictionary.json")
        except Exception as e:
            print("Exception when trying to read dictionary.json: {}".format(e.args))
        finally:
            eng_dict_f.close()
    
    # Remove all entries with multiple words, hyphenation, or apostrophes
    for word in words:
        if not bool(re.search(r'\s|-|\'', word)):
            words_new.append(word)
    
    return words_new


def loadWordsJSON(paths: []):
    words = []
    
    for path in paths:
        with open(path, encoding='utf-8') as words_f:
            try:
                words = json.load(words_f)
                print("Loaded and parsed ", words_f)
            except Exception as e:
                print("Exception while trying to read {}: {}".format(words_f, e.args))
            finally:
                words_f.close()
    
    return words
    

def isWordValid(input: str):
    return input in eng_dict


def loadModel():
    return KeyedVectors.load_word2vec_format('data/GoogleNews-vectors-negative300.bin.gz', limit=100000, binary=True, unicode_errors='ignore')


def getSimilarity(word: str, vectors):
    return cosine_similarity([vectors[word]], [vectors['lava']])[0][0]

eng_dict = loadEngDictionary()
vectors = loadModel()
print(getSimilarity('mountain', vectors))

import re
import json
from gensim.models import KeyedVectors
from sklearn.metrics.pairwise import cosine_similarity
import random


class WordHandler:
    # Words from Oxford dictionary
    eng_dict = []
    vectors = KeyedVectors.load_word2vec_format('data/GoogleNews-vectors-negative300.bin.gz', limit=100000, binary=True, unicode_errors='ignore')


    def __init__(self):
        self.eng_dict = self.loadEngDictionary()


    def loadEngDictionary(self):
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


    def loadWordsJSON(self, paths: []):
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


    def getRandomWord(self, wordList: []):
        return wordList[random.randint(0, len(wordList) - 1)]


    def isWordValid(self, input: str):
        return input.lower() in self.eng_dict


    def getSimilarity(self, word1: str, word2: str):
        try:
            return cosine_similarity([self.vectors[word1]], [self.vectors[word2]])[0][0]
        except KeyError:
            return 0


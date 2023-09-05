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

import words
from platform import system as pl_sys
from os import system as os_sys
from rich.console import Console
from rich.console import Theme
from rich.prompt import Prompt
from rich.prompt import Confirm
from pyfiglet import figlet_format
from operator import itemgetter

class Game:
    wordHandler = words.WordHandler()

    answers = []  # List of possible answers
    answer = ''   # Actual answer

    maxGuesses = 1  # Max allowed guesses for this game
    curGuesses = maxGuesses  # Current number of guesses
    categoriesPaths = []  # Selected word lists (paths) to load for this game

    hasWon = False

    textTheme = Theme({
        'default': 'grey85',
        'title': 'pink3',
        'subtitle': 'grey93',
        'green': 'dark_sea_green4',
        'yellow': 'light_goldenrod1',
        'red': 'red3'
    })

    guessColor = 'dark_sea_green4'
    guessedWords = {}


    def __init__(self, categoriesPaths: [], maxGuesses: int):
        self.categoriesPaths = categoriesPaths
        self.maxGuesses = maxGuesses
        self.curGuesses = maxGuesses
        self.answers = self.wordHandler.loadWordsJSON(self.categoriesPaths)
        self.answer = self.wordHandler.getRandomWord(self.answers)
        self.wordHandler.loadWordsJSON(categoriesPaths)


    def getGuessColor(self):
        if self.curGuesses / self.maxGuesses >= 0.75:
            return 'dark_sea_green4'
        elif self.curGuesses / self.maxGuesses < 0.75 and self.curGuesses / self.maxGuesses >= 0.25:
           return 'light_goldenrod1'
        elif self.curGuesses / self.maxGuesses < 0.25:
            return 'red3'


    def getSimScoreColor(self, score: float):
        if score >= 0.75:
            return 'dark_sea_green4'
        elif score >= 0.5 and score < 0.75:
            return 'light_goldenrod1'
        else:
            return 'red3'
    

    def clearScreen(self):
        CLEAR = 'cls' if pl_sys() == 'Windows' else 'clear'
        os_sys(CLEAR)


    # Title, description, and instructions
    def printIntro(self):
        self.clearScreen()

        console = Console(theme=self.textTheme, width=100)
        console.print(figlet_format('Contexto', font='big'), style='bold pink3')

        introText = "This is a Python clone of the game Semantle.\nThe goal of the game is \
to correctly guess a randomly selected word by guessing words. The game will \
tell you how semantically similar your word is to the secret answer. The score \
assigned to each guess may range from -1 to 1, where -1 would be the complete \
opposite of the secret word, and 1 would be the secret word itself.\nUse the scores \
as clues to guess more similar words.\n\nNot all words are valid. Valid input words \
come from the Oxford dictionary. Some examples of invalid words are plurals, proper \
nouns, many slang words, and acronyms.\n\nThe similarity score is obtained by using \
word embeddings with gensim Word2Vec where the cosine similarity is the returned score. \
\nPress ENTER to begin..."

        console.print(introText)
        input()


    def printGuessedWords(self):
        guessedWords = sorted(self.guessedWords.items(), key=itemgetter(1), reverse=True)

        for word in guessedWords:
            theme = Theme({'score': self.getSimScoreColor(word[1])})
            console = Console(theme=theme, width=20)
            console.print('{} : [score]{:.5f}[/score]'.format(word[0], word[1]), justify='right')


    def printRemainingGuesses(self):
        theme = Theme({'guess': self.getGuessColor()})
        console = Console(theme=theme)
        console.print('Guesses: [guess]{}[/guess]/{}'.format(self.curGuesses, self.maxGuesses))


    def printTurn(self):
        self.clearScreen()
 
        console = Console(theme=self.textTheme)
    
        console.print(figlet_format('Contexto', font='big'), style='bold pink3')
        console.print('Guess the correct word by guessing words with high similarity scores!\n')
        self.printRemainingGuesses()
        console.print('\nGuessed words:')
        self.printGuessedWords()

    
    def printWin(self):
        self.clearScreen()

        console = Console(theme=self.textTheme)
        
        console.print(figlet_format('Contexto', font='big'), style='bold pink3')
        console.print('The correct word was [green]{}[/green]!')
        console.print('\nYou won with ', end='')
        self.printRemainingGuesses()
        console.print(' guesses remaining.')

        self.printGuessedWords()
    

    def printLose(self):
        self.clearScreen()

        console = Console(theme=self.textTheme)

        print(figlet_format('Game Over', font='big'))
        console.print('You\'ve used all of your {} guess attempts'.format(self.maxGuesses))
        console.print('The correct word was [yellow]{}[/yellow].'.format(self.answer))

        tryAgain = Confirm.ask('Try again with a different word?')

        if tryAgain:
            self.curGuesses = self.maxGuesses
            self.hasWon = False
            self.guessedWords.clear()
            self.answer = self.wordHandler.getRandomWord(self.answers)
            self.startGame()
        else:
            quit()


    def guessWord(self):
        guess = Prompt.ask("\nGuess a word")

        if not self.wordHandler.isWordValid(guess):
            print("Word is not in vocabulary. Press ENTER to try again.")
            input()
            self.guessWord()
        elif guess in self.guessedWords:
            print("You've already guessed this word. Press ENTER to try again.")
            input()
            self.guessWord()
        else:
            guessScore = (guess, self.wordHandler.getSimilarity(guess, self.answer))
            self.guessedWords[guess] = guessScore[1]

            theme = Theme({'score': self.getSimScoreColor(guessScore[1])})
            console = Console(theme=theme)

            if guessScore[1] >= 1:
                self.hasWon = True
            else:
                self.curGuesses -= 1
                console.print("\n{} : [score]{:.5f}[/score]. Press ENTER to continue.".format(guessScore[0], guessScore[1]))
                input()
            

    def startGame(self):
        self.printIntro()

        while self.curGuesses > 0 and not self.hasWon:
            self.printTurn()
            self.guessWord()

        if self.curGuesses <= 0:
            self.printLose()
        elif self.hasWon:
            self.printWin()





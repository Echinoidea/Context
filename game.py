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
import colorama


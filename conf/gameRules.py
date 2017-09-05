###############################################################################
## Module name  : gameRules.py
## Author       : Andrew Laing (parisianconnections@gmail.com)
## Source       : Python 3.5
## Purpose      : This module contains the rules to the game
##                of Rock-Paper-Scissors-Spock-Lizard.
## History      : Work started 29/09/2015
###############################################################################

## choices - a list containing the choices available to the player in the game
choices      = ["Rock","Paper","Scissors","Spock","Lizard"]


## validGuesses - a list containing valid input strings (only the first two letters
##                of the players input are read in)
validGuesses = ["ro","pa","sc","sp","li"]


## winningChoices - a list containing the indexes of the options that will
##                  defeat ro,pa,sc,sp,li
winningChoices = [[1,3],[2,4],[0,3],[1,4],[0,2]]


## rules is used by RPSSL.calculateWinner() to decide who wins the round
##       and create the result string to print for the users
rules = { (0,0): {"winner": 0, "winStr": "Draw, nobody wins!"},
          (0,1): {"winner": 2, "winStr": "Paper covers Rock!"},
          (0,2): {"winner": 1, "winStr": "Rock smashes Scissors!"},
          (0,3): {"winner": 2, "winStr": "Spock vaporizes Rock!"},
          (0,4): {"winner": 1, "winStr": "Rock crushes Lizard!"},
          (1,0): {"winner": 1, "winStr": "Paper covers Rock!"},
          (1,1): {"winner": 0, "winStr": "Draw, nobody wins!"},
          (1,2): {"winner": 2, "winStr": "Scissors cut Paper!"},
          (1,3): {"winner": 1, "winStr": "Paper disproves Spock!"},
          (1,4): {"winner": 2, "winStr": "Lizard eats Paper!"},
          (2,0): {"winner": 2, "winStr": "Rock smashes Scissors!"},
          (2,1): {"winner": 1, "winStr": "Scissors cut Paper!"},
          (2,2): {"winner": 0, "winStr": "Draw, nobody wins!"},
          (2,3): {"winner": 2, "winStr": "Spock smashes Scissors!"},
          (2,4): {"winner": 1, "winStr": "Scissors decapitate Lizard!"},
          (3,0): {"winner": 1, "winStr": "Spock vaporizes Rock!"},
          (3,1): {"winner": 2, "winStr": "Paper disproves Spock!"},
          (3,2): {"winner": 1, "winStr": "Spock smashes Scissors!"},
          (3,3): {"winner": 0, "winStr": "Draw, nobody wins!"},
          (3,4): {"winner": 2, "winStr": "Lizard poisons Spock!"},
          (4,0): {"winner": 2, "winStr": "Rock crushes Lizard!"},
          (4,1): {"winner": 1, "winStr": "Lizard eats Paper!"},
          (4,2): {"winner": 2, "winStr": "Scissors decapitate Lizard!"},
          (4,3): {"winner": 1, "winStr": "Lizard poisons Spock!"},
          (4,4): {"winner": 0, "winStr": "Draw, nobody wins!"} }

###############################################################################
## Filename     : rpssl.py
## Author       : Andrew Laing (parisianconnections@gmail.com)
## Source       : Python 3.5
## Description  : The gameplay methods for the RPSSL application.
## History      : Work started 29/09/2015
###############################################################################

from random import randint
from random import choice as rndchoice
from os import path

for filename in ["utils.py","conf/gameRules.py","classifier.py"]:
    if not path.isfile(filename):
        print("Error: Configuration file '%s' not found."% filename)
        print("Exiting program.")
        exit()

from utils import saveToPickle, loadFromPickle
import conf.gameRules as gameRules
import classifier as rpsslClassifier


class RPSSL(object):
    def __init__(self, loadPk=0):
        """
        Init method for the RPSSL Class.
        Loads the configuration file or creates one.
        """
        loaded = 0
        
        # Autoload the configuration data stored in rpssl.pk
        if loadPk:
            self.__dict__ = loadFromPickle("conf/rpssl.pk")
            self.classifier = rpsslClassifier.naivebayes(loadPk=1)
            loaded = 1
        ## If rpssl.pk doesn't exist yet run the basic configuration
        if not loaded:
            self.maxRounds = 5
            self.choices = gameRules.choices
            self.validGuesses = gameRules.validGuesses
            self.winningChoices = gameRules.winningChoices
            self.rules = gameRules.rules

            # For implementing strategy 2. ####################################
            #  if using probablilty is losing, add the possiblity of a random
            #  choice being made by the bot
            self.strategy2percentage = 0.75
            self.sampleSize = 0   # total rounds played
            self.botWins   = 0    # total bot wins
            self.humanWins = 0    # total human wins

            ###################################################################

            ## Initialise round variables
            self.initCurrentGameVars()
            ## Initialise Intelligence variables
            self.initIntelligence()
            ## Create configuration file
            saveToPickle("conf/rpssl.pk", self.__dict__)
            self.classifier = rpsslClassifier.naivebayes()

        self.configChanged = 0 # Flag for configuation changes
        self.roundsPlayed = 0


    def initPlayerOneVars(self):
        """
        Initialising Player One variables.
        Called by self.__init__() and self.playNewGame()
        """
        self.playerOneGuess = 0
        self.playerOneScore = 0


    def initPlayerTwoVars(self):
        """
        Re/Initialise Player One variables.
        Called by self.__init__() and self.playNewGame()
        """
        self.playerTwoGuess = 0
        self.playerTwoScore = 0


    def initCurrentGameVars(self):
        """
        Re/Initialise Current Game variables.
        Called by self.__init__() and self.playNewGame()
        """
        self.initPlayerOneVars()
        self.initPlayerTwoVars()
        self.roundsPlayed = 0
        self.drawsScore = 0
        self.winner = 0
        self.winString = "Draw, Nobody wins!"


    def initIntelligence(self):
        """
        Initialise Intelligence variables.
        Called by self.__init__()
        """
        self.initHumanStats()
        self.initBotStats()


    def initHumanStats(self):
        """
        Initialise Human Statistic variables.
        Called by self.initIntelligence()
        """
        self.lastChoice        = None
        self.choiceBeforeLast  = None
        self.choice2BeforeLast = None


    def initBotStats(self):
        """
        Initialise Bot Statistic variables.
        Called by self.initIntelligence()
        """
        self.botLastChoice        = None
        self.botChoiceBeforeLast  = None
        self.botChoice2BeforeLast = None


    def saveOnQuit(self):
        """
        Save the configuration and classifier when quitting the app.
        """
        saveToPickle("conf/rpssl.pk", self.__dict__)
        self.classifier.saveCounts()


    ## INTELLIGENCE METHODS ###################################################

    def updateHumanStatsAndGetFeatures(self):
        """
        Update the stats stored for the human then create
        and return a list of features.
        Called by self.trainClassifier()
        """
        features = []
        # update stats kept on human
        prevLast    = self.lastChoice
        prevBefore  = self.choiceBeforeLast 
        prev2Before = self.choice2BeforeLast

        if self.choiceBeforeLast != None:
            self.choice2BeforeLast = self.choiceBeforeLast

        if self.lastChoice != None:
            self.choiceBeforeLast = self.lastChoice

        self.lastChoice = self.validGuesses[self.playerOneGuess]

        # Update features list with previous human choices
        if prevLast != None:
            features.append(prevLast)

            if prevBefore != None:
                temp = prevBefore+prevLast
                features.append(temp)

                if prev2Before != None:
                    temp = prev2Before+prevBefore+prevLast
                    features.append(temp)

        return features

        
    def updateBotStatsAndGetFeatures(self):
        """
        Update the stats stored for the bot then create
        and return a list of features.
        Called by self.trainClassifier()
        """
        features = []
        # update stats kept on bot
        prevLast    = self.botLastChoice
        prevBefore  = self.botChoiceBeforeLast 
        prev2Before = self.botChoice2BeforeLast

        if self.botChoiceBeforeLast != None:
            self.botChoice2BeforeLast = self.botChoiceBeforeLast

        if self.botLastChoice != None:
            self.botChoiceBeforeLast = self.botLastChoice

        self.botLastChoice = self.validGuesses[self.playerTwoGuess]

        # Update features list with previous bot choices
        if prevLast != None:
            temp = "b"+prevLast
            features.append(temp)

            if prevBefore != None:
                temp = "b"+prevBefore+prevLast
                features.append(temp)

                if prev2Before != None:
                    temp = "b"+prev2Before+prevBefore+prevLast
                    features.append(temp)

        return features


    def trainClassifier(self):
        """
        Send features and category to the classifier.
        Called by self.playGame()
        """
        features = self.updateHumanStatsAndGetFeatures()
        features.extend( self.updateBotStatsAndGetFeatures() )
        category = self.validGuesses[self.playerOneGuess]
        self.classifier.train(features, category)


    def getChoiceToDefeatHuman(self, guess):
        """
        Return an option which will defeat what the classifier
        has calculated that the human player will choose.
        Called by self.getBotChoice()
        """
        return rndchoice(self.winningChoices[guess])


    def getProbableHumanChoice(self):
        """
        Creates a list of features and sends them to the classifier
        to get a probable category.
        Called by self.getBotChoice()
        """
        features = []
        onemb = self.lastChoice
        bOnemb = self.botLastChoice
        
        if onemb!=None:
            features.append(onemb)
            if self.choiceBeforeLast!=None:
                twomb = self.choiceBeforeLast + onemb
                features.append(twomb)
                if self.choice2BeforeLast!=None:
                    threemb = self.choice2BeforeLast + twomb     
                    features.append(threemb)

        if bOnemb!=None:
            features.append("b"+bOnemb)
            if self.botChoiceBeforeLast!=None:
                bTwomb = self.botChoiceBeforeLast + bOnemb
                features.append("b"+bTwomb)
                if self.botChoice2BeforeLast!=None:
                    bThreemb = self.botChoice2BeforeLast + bTwomb     
                    features.append("b"+bThreemb)

        guess = randint(0,len(self.validGuesses)-1)
        default = self.validGuesses[guess]

        best = self.convertGuessToInt(self.classifier.classify(features,default))

        return best


    def getBotChoice(self, player):
        """
        Get and return the bot's choice.
        Called by self.playARound()
        """
        ## Get a number that is an index to the validGuesses list
        ## using the naivebayesian classifier

        if self.humanWins > (self.sampleSize * self.strategy2percentage):
            baseline = ((self.humanWins/float(self.sampleSize)) * 40) # if rand < this
            if randint(0,100) < baseline:
                guess = randint(0,len(self.validGuesses)-1)
            else:
                guess = self.getProbableHumanChoice()
            choice = self.getChoiceToDefeatHuman(guess)
        else:
            guess = self.getProbableHumanChoice()
            choice = self.getChoiceToDefeatHuman(guess)

        return choice


    ## GAMEPLAY METHODS #######################################################

    def adjustScores(self):
        """
        Adjust the stored scores for the current game.
        Called by self.playGame()
        """
        ## Augment the winner's score
        if self.winner==1:
            self.playerOneScore+=1
            self.humanWins+=1
        elif self.winner==2:
            self.playerTwoScore+=1
            self.botWins+=1
        elif self.winner==0: self.drawsScore+=1

        self.sampleSize+=1


    def calculateWinner(self):
        """
        Calculate winner of round and update round winner data.
        Called by self.playGame()
        """
        ## Create a tuple representing the player's choices
        rulesKey = (self.playerOneGuess,self.playerTwoGuess)
        ## Find the winner from the rules dictionary
        self.winner    = self.rules[rulesKey]["winner"]
        self.winString = self.rules[rulesKey]["winStr"]
        if self.winner==1:
            self.winString += "\nPlayer wins!"
        elif self.winner==2:
            self.winString += "\nBot wins!"


    def convertGuessToInt(self, guess):
        """
        Convert the player's guess string to an integer.
        Called by self.getHumanChoice() and self.getProbableHumanChoice()
        """
        return self.validGuesses.index(guess)


    def playARound(self, guess):
        """
        Play a whole round.
        Called by self.playGame()
        """
        self.playerOneGuess=self.convertGuessToInt(guess)
        self.playerTwoGuess=self.getBotChoice(2)


    def getGameResult(self):
        """
        Return the result of the Game as a string.
        """
        ## Create a string containing the final score
        score = "%d:%d" % (self.playerOneScore,self.playerTwoScore)
        ## Find out who won the game using conditional operator comparisons
        ## And return the result
        result = ""
        if self.playerOneScore > self.playerTwoScore:
            result += "Player has won the game!"
        elif self.playerTwoScore > self.playerOneScore:
            result += "Bot has won the game!"
        else: result += "The game was drawn!"
        result += "\nThe final score was " + score

        return result


    def playGame(self, choice):
        """
        Play a game.
        """
        self.playARound(choice) 
        self.calculateWinner()
        self.adjustScores()
        ## update the stats and train the classifier
        self.trainClassifier()

        self.roundsPlayed += 1
        if self.roundsPlayed == self.maxRounds:
            self.classifier.saveCounts()


    def startGame(self):
        """
        Clear screen and start a new game.
        """
        ## Reset the gameplay variables to their initial state
        self.initCurrentGameVars()
            
        saveToPickle("conf/rpssl.pk", self.__dict__)


    def changeMaxRounds(self, n):
        """
        Change number of rounds per game.
        """
        self.configChanged = 1
        self.maxRounds = n


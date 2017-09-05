###############################################################################
## Module name  : utils.py
## Author       : Andrew Laing (parisianconnections@gmail.com)
## Source       : Python 3.5
## Purpose      : Storage methods used by the game.
## History      : Work started 29/09/2015
###############################################################################

import pickle

def saveToPickle(filename, toWrite):
    """
    Writes out the object passed to it into a pickle.
    """
    output = open(filename,'wb')
    pickle.dump(toWrite, output, -1)
    output.close()


def loadFromPickle(filename):
    """
    Return object from pickle file.
    """
    input1 = open(filename,'rb')
    toLoad = pickle.load(input1)
    input1.close()
    return toLoad

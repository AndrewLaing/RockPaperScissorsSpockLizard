###############################################################################
## Filename     : classifier.py
## Author       : Andrew Laing (parisianconnections@gmail.com)
## Source       : Python 3.5
## Description  : Naive Bayesian Classifier used to help the bot learn how
##                to defeat the player.
## History      : Work started 29/09/2015
###############################################################################


from utils import saveToPickle, loadFromPickle

class naivebayes(object):
    """
    naivebayes classifier class.
    """
    def __init__(self, loadPk=0):
        if loadPk:
            toUnload = loadFromPickle("conf/naivebayes.pk")
            self.cc = toUnload["cc"]
            self.fc = toUnload["fc"]
        else:
            self.fc={}
            self.cc={}
            self.saveCounts()


    def saveCounts(self):
        """
        Save the count dictionaries cc and fc to cPickle.
        Called by self.__init__() and rpssl.mainMenu()
        """
        toSave = {"cc": self.cc, "fc": self.fc}
        saveToPickle("conf/naivebayes.pk", toSave)


    def incf(self,f,cat):
        """
        Increases the count in fc of a feature/category pair.
        Called by self.train()
        """
        self.fc.setdefault(f,{})
        self.fc[f].setdefault(cat,0)
        self.fc[f][cat]+=1


    def incc(self,cat):
        """
        Increases the count in cc of a category.
        Called by self.train()
        """
        self.cc.setdefault(cat,0)
        self.cc[cat]+=1


    def fcount(self,f,cat):
        """
        Returns the number of times that a feature has appeared
        in a category from fc.
        Called by self.fprob() and self.weightedprob()
        """
        if f in self.fc and cat in self.fc[f]:
            return float(self.fc[f][cat])
        return 0.0


    def catcount(self,cat):
        """
        Returns the number of items in a category from cc.
        Called by self.fprob() and naivebayes.prob()
        """
        if cat in self.cc:
            return float(self.cc[cat])
        return 0


    def totalcount(self):
        """
        Returns the total number of unique items kept in cc.
        Called by naivebayes.prob()
        """
        return sum(self.cc.values())


    def categories(self):
        """
        Returns a list of all the categories in cc.
        called by self.weightedprob() and naivebayes.classify()
        """
        return self.cc.keys()


    def train(self,features,cat):
        """
        Trains the classifier by incrementing the counts in cc and fc.
        Called by rpssl.trainClassifier()
        """
        for f in features:
            self.incf(f,cat)

        self.incc(cat)


    def fprob(self,f,cat):
        """
        Return the probability of a feature appearing in a category.
        Called by naivebayes.docprob()
        """
        if self.catcount(cat)==0: return 0
        return self.fcount(f,cat)/self.catcount(cat)


    # ap = assumed probability - 0.2 because there are 5 choices with equal
    #                            probability of being chosen
    def weightedprob(self,f,cat,prf,weight=1.0,ap=0.2):
        """
        Returns the weighted probability of a feature in a category.
        Called by naivebayes.docprob()
        """
        # Calculate current probability
        basicprob=prf(f,cat)
        # Count the number of times this feature has appeared in all categories
        totals=sum([self.fcount(f,c) for c in self.categories()])
        # Calculate the weighted average
        bp=((weight*ap)+(totals*basicprob))/(weight+totals)
        return bp


    def docprob(self,features,cat):
        """
        Returns the probabilty of the category existing in all features
        Called by self.prob()
        """
        p=1
        for f in features: p *= self.weightedprob(f,cat,self.fprob)
        return p


    def prob(self,features,cat):
        """
        Returns the calculated probability for the category supplied.
        Called by self.classify() 
        """
        catprob=self.catcount(cat)/self.totalcount()
        docprob=self.docprob(features,cat)
        return docprob*catprob


    def classify(self,features,default="ro"):
        """
        Returns the category with the highest probability
        calculated from the supplied features.
        Called by rpssl.getProbableHumanChoice()
        """
        probs={}
        best=default
        # Find the category with the highest probability
        max=0.0
        for cat in self.categories():
            probs[cat]=self.prob(features,cat)
            if probs[cat]>max:
                max=probs[cat]
                best=cat

        return best

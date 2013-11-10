import ols
import numpy as np
from tools.loadData import loadStock
from tools import crossValidation as cv
from tools.writePath import createPath

class SRFeatures():
    def __init__(self):
        pass

    def setFeatures(self, features):
        self.prices = []
        self.ema = []
        
        for stats in features:
            self.prices.append(stats['price'])
            self.ema.append(stats['ema'])

    def findSol(self, windowSize):
        y = np.array(self.prices)
        x = np.vstack([self.ema]).T
        
        mymodel = ols.ols(y,x,'price',['EMA'])

        labels = ['constant', 'EMA']
        
        equation = "price(t+1) = "
        
        stats = {}
        
        for i in range(len(mymodel.b)):
            l = labels[i]
            c = mymodel.b[i]
            stats[l] = c
            if l == 'constant':
                equation += str(c) + " + "
            else:
                equation += str(c) + "*" + l + "(t) + "
        equation = equation[:-2]
        
        return stats

stocks = ['C', 'FDX', 'KO', 'MSFT', 'SBUX', 'NFLX', 'LUV']

for s in stocks:
    path = createPath(s + '/' + s + 'emaValidation.csv')
    featuresPath  = createPath(s + '/')
    cv.simpleCrossValidationFeatures(featuresPath, path, SRFeatures())
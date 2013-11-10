import ols
import numpy as np
from tools import crossValidation as cv
from tools.writePath import createPath

class MRFeatures():
    def __init__(self):
        pass

    def setFeatures(self, features):
        self.prices = []
        self.ema = []
        self.rsi = []
        self.macd = []
        
        for stats in features:
            self.prices.append(stats['price'])
            self.ema.append(stats['ema'])
            self.rsi.append(stats['rsi'])
            self.macd.append(stats['macd'])

    def findSol(self, windowSize):
        y = np.array(self.prices)
        x = np.vstack([self.ema, self.rsi, self.macd]).T
        
        mymodel = ols.ols(y,x,'price',['EMA','RSI','MACD'])
        
        labels = ['constant', 'EMA','RSI','MACD']
        
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
    path = createPath(s + '/' + s + 'mrValidation.csv')
    featuresPath  = createPath(s + '/')
    cv.crossValidationFeatures(featuresPath, path, MRFeatures())
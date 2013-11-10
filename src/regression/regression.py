import ols
import numpy as np
from tools.loadData import loadStock
from tools import crossValidation as cv
from tools.writePath import createPath

class MultipleRegression():
    def __init__(self):
        pass

    def setFeatures(self, features):
        self.tf = features

    def findSol(self, windowSize):
        prices, ema, rsi, macd = self.tf.getTimewindow(windowSize)
        y = np.array(prices)
        x = np.vstack([ema, rsi, macd]).T
        
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

stocks = ['NFLX', 'LUV']

for s in stocks:
    timeseries = loadStock(s + '/' + s)
    path = createPath(s + '/' + s + 'mrValidation.csv')
    featuresPath  = createPath(s + '/')
    cv.crossValidationFeatures(featuresPath, path, timeseries, MultipleRegression())
import csv
from itertools import izip
from collections import OrderedDict
#from ordereddict import OrderedDict
from tools import anova
from tools import technicalFeatures as tf
from tools.loadData import loadFeatures
import numpy as np

# from http://code.activestate.com/recipes/521906-k-fold-cross-validation-partition/
def k_fold_cross_validation(X, K, randomise = False):
    """
    Generates K (training, validation) pairs from the items in X.

    Each pair is a partition of X, where validation is an iterable
    of length len(X)/K. So each training iterable is of length (K-1)*len(X)/K.

    If randomise is true, a copy of X is shuffled before partitioning,
    otherwise its order is preserved in training and validation.
    """
    if randomise: from random import shuffle; X=list(X); shuffle(X)
    for k in xrange(K):
        training = [x for i, x in enumerate(X) if i % K != k]
        validation = [x for i, x in enumerate(X) if i % K == k]
        yield training, validation

def crossValidation(filename, timeseries, algorithm, k=10):
    csvFile = open(filename, 'a')
    f = csv.writer(csvFile)
    f.writerow(['t', 'constant', 'EMA', 'RSI' , 'MACD', 'R^2', 'AIC'])
    
    timeseries = timeseries.items()
    table = {}
    
    for training, validation in k_fold_cross_validation(timeseries, k):
        
        trainingDict = OrderedDict()
        for key, value in training:
            trainingDict[key] = value
            
        validationDict = OrderedDict()
        for key, value in validation:
            validationDict[key] = value
        
        tr = tf.TechnicalFeatures(trainingDict)
        vd = tf.TechnicalFeatures(validationDict)
        algorithm.setFeatures(tr)
        
        for i in range(2, 202, 2):
            sol = algorithm.findSol(i)
            prices, ema, rsi, macd = vd.getTimewindow(i)
            y = np.array(prices)
            x = np.vstack([ema, rsi, macd]).T
            
            validationStats = anova.ols(y, x, [sol['constant'], sol['EMA'], sol['RSI'], sol['MACD']])
            r2 = validationStats.R2
            aic = validationStats.ll()[1]
            
            # average out the results over k folds
            stats = [sol['constant'], sol['EMA'], sol['RSI'], sol['MACD'], r2, aic]
            stats = [val/float(k) for val in stats]
            
            if i in table:
                table[i] = [sum(item) for item in izip(table[i], stats)]
            else:
                table[i] = stats
            
            print i
            print stats
            
    # write the averaged results        
    for i in range(2, 202, 2):
        table[i].insert(0, i)
        print table[i]     
        f.writerow(table[i])
        csvFile.flush()

def simpleCrossValidation(filename, timeseries, algorithm, k=10):
    csvFile = open(filename, 'a')
    f = csv.writer(csvFile)
    f.writerow(['t', 'constant', 'EMA', 'R^2', 'AIC'])
    
    timeseries = timeseries.items()
    table = {}
    
    for training, validation in k_fold_cross_validation(timeseries, k):
        
        trainingDict = OrderedDict()
        for key, value in training:
            trainingDict[key] = value
            
        validationDict = OrderedDict()
        for key, value in validation:
            validationDict[key] = value
        
        tr = tf.TechnicalFeatures(trainingDict)
        vd = tf.TechnicalFeatures(validationDict)
        algorithm.setFeatures(tr)
        
        for i in range(2, 202, 2):
            sol = algorithm.findSol(i)
            prices, ema, rsi, macd = vd.getTimewindow(i)
            
            y = np.array(prices)
            x = np.vstack([ema]).T
               
            validationStats = anova.ols(y, x, [sol['constant'], sol['EMA']])
            r2 = validationStats.R2
            aic = validationStats.ll()[1]
            
            # average out the results over k folds
            stats = [sol['constant'], sol['EMA'], r2, aic]
            stats = [val/float(k) for val in stats]
            
            if i in table:
                table[i] = [sum(item) for item in izip(table[i], stats)]
            else:
                table[i] = stats
            
            print i
            print stats
            
    # write the averaged results        
    for i in range(2, 202, 2):
        table[i].insert(0, i)
        print table[i]     
        f.writerow(table[i])
        csvFile.flush()

def crossValidationFeatures(featureLocation, filename, algorithm, k=10):
    
    csvFile = open(filename, 'a')
    f = csv.writer(csvFile)
    f.writerow(['t', 'constant', 'EMA', 'RSI' , 'MACD', 'R^2', 'AIC'])
    
    table = {}
    
    for i in range(2, 202, 2):
        
        features = loadFeatures(featureLocation, i)
        bestSol = []
        bestR2 = 0
        
        for training, validation in k_fold_cross_validation(features, k):
            
            algorithm.setFeatures(training)
            sol = algorithm.findSol(i)
            
            prices = []
            ema = []
            rsi = []
            macd = []

            for row in validation:
                prices.append(row['price'])
                ema.append(row['ema'])
                rsi.append(row['rsi'])
                macd.append(row['macd'])
            
            y = np.array(prices)
            x = np.vstack([ema, rsi, macd]).T
            
            validationStats = anova.ols(y, x, [sol['constant'], sol['EMA'], sol['RSI'], sol['MACD']])
            r2 = validationStats.R2
            aic = validationStats.ll()[1]
            
            if (r2 > bestR2):
                bestR2 = r2
                bestSol = [sol['constant'], sol['EMA'], sol['RSI'], sol['MACD']]
            
            # average out the results over k folds
            stats = [r2, aic]
            stats = [val/float(k) for val in stats]
            
            if i in table:
                table[i] = [sum(item) for item in izip(table[i], stats)]
            else:
                table[i] = stats
        
        for j in range(len(bestSol)):
            table[i].insert(j, bestSol[j])
            
        print i
        # write the averaged results        
        table[i].insert(0, i)
        print table[i]     
        f.writerow(table[i])
        csvFile.flush()

def simpleCrossValidationFeatures(featureLocation, filename, algorithm, k=10):
    csvFile = open(filename, 'a')
    f = csv.writer(csvFile)
    f.writerow(['t', 'constant', 'EMA', 'R^2', 'AIC'])
    
    table = {}
        
    for i in range(2, 202, 2):
        features = loadFeatures(featureLocation, i)
        bestSol = []
        bestR2 = 0
        
        for training, validation in k_fold_cross_validation(features, k):
            algorithm.setFeatures(training)
            sol = algorithm.findSol(i)
            
            prices = []
            ema = []

            for row in validation:
                prices.append(row['price'])
                ema.append(row['ema'])
            
            y = np.array(prices)
            x = np.vstack([ema]).T
               
            validationStats = anova.ols(y, x, [sol['constant'], sol['EMA']])
            r2 = validationStats.R2
            aic = validationStats.ll()[1]
            
            if (r2 > bestR2):
                bestR2 = r2
                bestSol = [sol['constant'], sol['EMA']]
            
            # average out the results over k folds
            stats = [r2, aic]
            stats = [val/float(k) for val in stats]
            
            if i in table:
                table[i] = [sum(item) for item in izip(table[i], stats)]
            else:
                table[i] = stats
            
            print i
            print stats
            
            
        for j in range(len(bestSol)):
            table[i].insert(j, bestSol[j])
            
    # write the averaged results        
    for i in range(2, 202, 2):
        table[i].insert(0, i)
        print table[i]     
        f.writerow(table[i])
        csvFile.flush()
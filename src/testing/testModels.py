import copy
from tools.loadData import createPath, loadModels, loadTestResults
from tools.writePath import createTestingPath
import csv
from itertools import izip
from tools import anova
from tools.loadData import loadFeatures
import numpy as np

'''
Created on May 16, 2011

@author: bash125
'''
    
def emaTest(filename):
    
    stocks = ['C', 'FDX', 'KO', 'MSFT', 'SBUX', 'NFLX', 'LUV']
    
    for s in stocks:
        
        csvFile = open(s+filename, 'a')
        f = csv.writer(csvFile)
        
        table = {}
        
        f.writerow([s])
        f.writerow(['t', 'R^2', 'AIC'])
        path = createPath(s + '/' + s + 'emaValidation.csv')    
        models = loadModels(path, "emaOnly")
        
        remainingStocks = copy.deepcopy(stocks)
        remainingStocks.remove(s)
        for line in models:
            
            for rs in remainingStocks:
                i = line['timewindow']
                
                featurePath = createPath(rs + "/")
                features = loadFeatures(featurePath, i)
                
                prices = []
                ema = []
    
                for row in features:
                    prices.append(row['price'])
                    ema.append(row['ema'])
                
                y = np.array(prices)
                x = np.vstack([ema]).T
                
                validationStats = anova.ols(y, x, [line['constant'], line['ema']])
                r2 = validationStats.R2
                aic = validationStats.ll()[1]
                # average out the results over k folds
                stats = [r2, aic]
                stats = [val/float(len(remainingStocks)) for val in stats]
                
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

def mrTest(filename):
    
    stocks = ['C', 'FDX', 'KO', 'MSFT', 'SBUX', 'NFLX', 'LUV']
    
    for s in stocks:
        csvFile = open(s+filename, 'a')
        f = csv.writer(csvFile)
        
        table = {}
        
        f.writerow([s])
        f.writerow(['t', 'R^2', 'AIC'])
        path = createPath(s + '/' + s + 'mrValidation.csv')    
        models = loadModels(path, "mr")
        
        remainingStocks = copy.deepcopy(stocks)
        remainingStocks.remove(s)
        for line in models:
            
            for rs in remainingStocks:
                i = line['timewindow']
                
                featurePath = createPath(rs + "/")
                features = loadFeatures(featurePath, i)
                
                prices = []
                ema = []
                rsi = []
                macd = []
    
                for row in features:
                    prices.append(row['price'])
                    ema.append(row['ema'])
                    rsi.append(row['rsi'])
                    macd.append(row['macd'])
                
                y = np.array(prices)
                x = np.vstack([ema, rsi, macd]).T
                
                validationStats = anova.ols(y, x, [line['constant'], line['ema'], line['rsi'], line['macd']])
                r2 = validationStats.R2
                aic = validationStats.ll()[1]
                # average out the results over k folds
                stats = [r2, aic]
                stats = [val/float(len(remainingStocks)) for val in stats]
                
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

def gaTest(filename):
    
    stocks = ['C', 'FDX', 'KO', 'MSFT', 'SBUX', 'NFLX', 'LUV']
    
    for s in stocks:
        csvFile = open(s+filename, 'a')
        f = csv.writer(csvFile)
        
        table = {}
        
        f.writerow([s])
        f.writerow(['t', 'R^2', 'AIC'])
        path = createPath(s + '/' + s + 'regularEvolution.csv')    
        models = loadModels(path, "ga")
        
        remainingStocks = copy.deepcopy(stocks)
        remainingStocks.remove(s)
        for line in models:
            
            for rs in remainingStocks:
                i = line['timewindow']
                
                featurePath = createPath(rs + "/")
                features = loadFeatures(featurePath, i)
                
                prices = []
                ema = []
                rsi = []
                macd = []
    
                for row in features:
                    prices.append(row['price'])
                    ema.append(row['ema'])
                    rsi.append(row['rsi'])
                    macd.append(row['macd'])
                
                y = np.array(prices)
                x = np.vstack([ema, rsi, macd]).T
                
                validationStats = anova.ols(y, x, [line['constant'], line['ema'], line['rsi'], line['macd']])
                r2 = validationStats.R2
                aic = validationStats.ll()[1]
                # average out the results over k folds
                stats = [r2, aic]
                stats = [val/float(len(remainingStocks)) for val in stats]
                
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
 
def coevolveTest(filename):
    
    stocks = ['C', 'FDX', 'KO', 'MSFT', 'SBUX', 'NFLX', 'LUV']
    
    for s in stocks:
        csvFile = open(s+filename, 'a')
        f = csv.writer(csvFile)
        
        table = {}
        
        f.writerow([s])
        f.writerow(['t', 'R^2', 'AIC'])
        path = createPath(s + '/' + s + 'coevolve.csv')    
        models = loadModels(path, "coevolve")
        
        remainingStocks = copy.deepcopy(stocks)
        remainingStocks.remove(s)
        for line in models:
            
            for rs in remainingStocks:
                i = line['timewindow']
                
                featurePath = createPath(rs + "/")
                features = loadFeatures(featurePath, i)
                
                prices = []
                ema = []
                rsi = []
                macd = []
    
                for row in features:
                    prices.append(row['price'])
                    ema.append(row['ema'])
                    rsi.append(row['rsi'])
                    macd.append(row['macd'])
                
                y = np.array(prices)
                x = np.vstack([ema, rsi, macd]).T
                
                validationStats = anova.ols(y, x, [line['constant'], line['ema'], line['rsi'], line['macd']])
                r2 = validationStats.R2
                aic = validationStats.ll()[1]
                # average out the results over k folds
                stats = [r2, aic]
                stats = [val/float(len(remainingStocks)) for val in stats]
                
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

def aggregateResults(filename):
    
    stocks = ['C', 'FDX', 'KO', 'MSFT', 'SBUX', 'NFLX', 'LUV']
    testResults = ['coevolveTesting', 'emaTesting', 'gaTesting', 'mrTesting']
    table = {}
    
    for model in testResults:
        
        csvFile = open(model + filename, 'a')
        f = csv.writer(csvFile)
        f.writerow(['t', 'R^2', 'AIC'])
        
        table = {}
        
        for s in stocks:
            path = createTestingPath(s + model + '.csv')    
            testResults = loadTestResults(path)
            
            for result in testResults:
                i = result[0]
                
                # average out the results over k folds
                stats = [result[1], result[2]]
                stats = [val/float(len(stocks)) for val in stats]
                
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

        
#emaTest("emaTesting.csv")
#mrTest("mrTesting.csv")
#gaTest("gaTesting.csv")
#coevolveTest("coevolveTesting.csv")
aggregateResults("aggregate.csv")
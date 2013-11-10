import csv
from collections import OrderedDict
#from ordereddict import OrderedDict
from writePath import createPath

def loadFile(filename):
    indexLevel=OrderedDict()
    f = csv.reader(open(filename))
    
    count = 0
    
    for line in f:
        if count > 0:
            date,openPrice,high,low,close,volume,adjClose=line
            indexLevel[date] = {'openPrice': float(openPrice),
                                'high': float(high),
                                'low': float(low),
                                'close': float(close),
                                'volume': float(volume),
                                'adjClose': float(adjClose)
                                
                                }
        count += 1
        
    return indexLevel

def loadFeatures(filepath, timewindow):
    
    filename = createPath(filepath, 'Timewindow Features', 'CSV', 'timewindowFeatures' + str(timewindow) + '.csv')
    f = csv.reader(open(filename))
    
    featuresList = []
    
    count = 0
    
    for line in f:
        if count > 0:
            day,price,ema,rsi,macd=line
            featuresList.append({'price': float(price),
                                'ema': float(ema),
                                'rsi': float(rsi),
                                'macd': float(macd)
                                })
        count += 1
        
    return featuresList

def loadModels(filepath, modelType):
    
    filename = createPath(filepath)
    f = csv.reader(open(filename))
    
    models = []
    
    count = 0
    
    for line in f:
        if count > 0:
            
            if modelType == "emaOnly":
            
                timewindow,constant,ema,R2,AIC=line
                models.append({'timewindow': int(timewindow),
                               'constant': float(constant),
                               'ema': float(ema)
                                    })
                
            elif modelType == "mr":
            
                timewindow,constant,ema,rsi, macd, R2,AIC=line
                models.append({'timewindow': int(timewindow),
                               'constant': float(constant),
                               'ema': float(ema),
                               'rsi': float(rsi),
                               'macd': float(macd)
                                    })
                
            elif modelType == "ga":
            
                timewindow = line[0].strip('"')
                constant = line[3].strip('"')
                ema = line[4].strip('"')
                rsi = line[5].strip('"')
                macd = line[6].strip('"')
                
                models.append({'timewindow': int(float(timewindow)),
                               'constant': float(constant),
                               'ema': float(ema),
                               'rsi': float(rsi),
                               'macd': float(macd)
                                    })
                
            elif modelType == "coevolve":
            
                timewindow = line[1].strip('"')
                constant = line[6].strip('"')
                ema = line[7].strip('"')
                rsi = line[8].strip('"')
                macd = line[9].strip('"')
                
                models.append({'timewindow': int(float(timewindow)),
                               'constant': float(constant),
                               'ema': float(ema),
                               'rsi': float(rsi),
                               'macd': float(macd)
                                    })    
        count += 1
        
    return models

            
            
def loadTestResults(filename):
    
    f = csv.reader(open(filename))
    
    results = []
    
    count = 0
    
    for line in f:
        if count > 1:
            timewindow,R2,AIC=line
            timewindow = int(timewindow)
            R2 = float(R2)
            AIC = float(AIC)
            results.append((timewindow, R2, AIC))
        count += 1
        
    return results

def loadStock(ticker):
    path = createPath(ticker + '.csv')
    return loadFile(path)

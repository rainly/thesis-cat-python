'''
Created on Apr 11, 2011

@author: bash125
'''

from tools.loadData import loadStock, createPath 
import os
from tools import technicalFeatures as tf

stocks = ['C', 'FDX', 'MSFT', 'SBUX', 'NFLX', 'LUV']

def ensure_dir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)

for s in stocks:
    timeseries = loadStock(s + '/' + s)
    path = createPath(s + '/' + 'Timewindow Features')
    ensure_dir(path)
    path += '/CSV/'
    ensure_dir(path)
    twf = tf.TechnicalFeatures(timeseries)
    for i in range(2, 202, 2):
        twf.setTimewindow(i)
        csvFile = path + 'timewindowFeatures' + str(i) + '.csv'
        twf.writeCsv(csvFile, twf.prices, twf.ema, twf.rsi, twf.macd)
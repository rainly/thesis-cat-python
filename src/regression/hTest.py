'''
Created on Mar 21, 2011

@author: bash125
'''
import fisherTransformation as ft
import csv
import math
from tools.writePath import createPath

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def loadFile(filename, alpha):
    f = csv.reader(open(filename))
    w = csv.writer(open('hTests.csv', 'w'))
    
    count = 0
    w.writerow(['t', 'mr-EMA z', 'GA-MR z', 'criticalZ'])
    for line in f:
        if count > 0:
            
            t,formula,e1R2,emaR2,mrR2,e1AIC, emaAIC,mrAIC,e2R2, e2AIC = line
            
            path = createPath('Timewindow Features', 'timewindowFeatures' + str(t) + '.csv')
 
            n = file_len(path)
            
            z1 = ft.fisherTransformation(math.sqrt(float(mrR2)), math.sqrt(float(emaR2)), n, n)
            z1, criticalZ, hTest = ft.normHTest(z1, alpha)
            
            z2 = ft.fisherTransformation(math.sqrt(float(e1R2)), math.sqrt(float(mrR2)), n, n)
            z2, criticalZ, hTest = ft.normHTest(z2, alpha)
            
            w.writerow([t, z1, z2, criticalZ])
        count += 1
        
path = createPath('modelsComparison.csv')
loadFile(path, 0.05)
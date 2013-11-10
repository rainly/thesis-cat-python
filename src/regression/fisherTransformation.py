'''
Created on Mar 21, 2011

@author: bash125
'''

import numpy
from scipy.stats import norm

def fisherTransformation(r1, r2, n1, n2):
    z1 = numpy.arctanh(r1)
    z2 = numpy.arctanh(r2)
    
    se = numpy.sqrt(1/(float(n1)-3) + 1/(float(n2)-3))
    
    z = (z1-z2)/se
    
    return z

def normHTest(z, alpha):
    criticalZ = norm.ppf(1-alpha)
    return z, criticalZ, z > criticalZ


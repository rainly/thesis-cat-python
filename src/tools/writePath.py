import os
'''
Created on Mar 25, 2011

@author: bash125
'''
def createPath(*args):
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', *args)
    return path


def createTestingPath(*args):
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'testing', *args)
    return path
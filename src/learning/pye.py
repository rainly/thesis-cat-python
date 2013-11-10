from pyevolve import G1DList
from pyevolve import GSimpleGA
from pyevolve import Selectors
from pyevolve import DBAdapters
from pyevolve import Initializators
from pyevolve import Mutators
from pyevolve import Crossovers
from pyevolve import Consts
import pyevolve

from tools import crossValidation as cv
from tools.writePath import createPath
from tools.loadData import loadStock

class GAForecaster():
    def __init__(self):
        self.time = 0
    
    def setFeatures(self, features):
        self.features = features
        
    def eval_func(self, features):
    
        def calcScore(chromosome):
            
            score = 0.0
            constant, ema, rsi, macd = chromosome
            
            for row in features:
                calcPrice = constant + ema*row['ema'] + rsi*row['rsi'] + macd*row['macd']
                residual = row['price'] - calcPrice
                
                # least square residuals
                score += (residual**2)
             
            return score
            
        return calcScore

    def findSol(self, timewindow):
        
        pyevolve.logEnable()
        genome = G1DList.G1DList(4)
        
        # range is constrained by the solutions found by MR
        genome.setParams(rangemin=-12.0, rangemax=2.0)
        # Change the initializator to Real Values
        genome.initializator.set(Initializators.G1DListInitializatorReal)
        # Change the mutator to Gaussian
        genome.mutator.set(Mutators.G1DListMutatorRealGaussian)
        # The evaluator function (objective function)
        genome.evaluator.set(self.eval_func(self.features))
        genome.crossover.set(Crossovers.G1DListCrossoverTwoPoint)
        
        # Genetic Algorithm Instance
        ga = GSimpleGA.GSimpleGA(genome)
        # Set the Roulette Wheel selector method, the number of generations and
        # the termination criteria
        ga.selector.set(Selectors.GRouletteWheel)
        
        # set default parameters for the engine
        ga.setGenerations(100) 
        #ga.setPopulationSize(80)
        #ga.setMutationRate(0.2)
        #ga.setCrossoverRate(0.8)
        ga.setMinimax(Consts.minimaxType["minimize"])
        ga.setElitism(True)
        ga.terminationCriteria.set(GSimpleGA.ConvergenceCriteria)
        
        # Sets the DB Adapter, the resetDB flag will make the Adapter recreate
        # the database and erase all data every run, you should use this flag
        # just in the first time, after the pyevolve.db was created, you can
        # omit it.
        
        #sqlite_adapter = DBAdapters.DBSQLite(identify="ex1", resetDB=True)
        dbPath = createPath('pyevolve.db')
        sqlite_adapter = DBAdapters.DBSQLite(dbname=dbPath, identify="timewindow" + str(timewindow), resetIdentify=True, resetDB=False)
        ga.setDBAdapter(sqlite_adapter)
        
        # Do the evolution, with stats dump frequency of 20 generations
        ga.evolve(freq_stats=20)
        
        # Best individual
        best = ga.bestIndividual()
        stats = {'constant': best[0],
                'EMA': best[1],
                'RSI': best[2],
                'MACD': best[3]
                }
        return stats

filename = createPath('gaValidation.csv')
timeseries = loadStock('KO')
cv.crossValidationFeatures(filename, GAForecaster())
import numpy as np
from itertools import islice, izip
import csv

class TechnicalFeatures():
    def __init__(self, timeseries):
        self.timeseries = timeseries
    
    def getPriceWindows(self, days):
        
        # from http://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks-in-python
        def chunks(l, n):
            """ Yield successive n-sized chunks from l.
            """
            for i in xrange(0, len(l), n):
                yield l[i:i+n]
        
        prices = [i['adjClose'] for i in self.timeseries.values()]
        prices.reverse()
        
        timewindow = list(chunks(prices, days))
        return timewindow
    
    def getAllPrices(self):
        prices = [i['adjClose'] for i in self.timeseries.values()]
        prices.reverse()
        return prices
    
    def simpleMovingAverage(self, days):
        pricewindow = self.getPriceWindows(days)
        sma = [sum(i)/days for i in pricewindow]
        return sma
    
    # from http://matplotlib.sourceforge.net/examples/pylab_examples/finance_work2.html
    def exponentialMovingAverage(self, n):
        """
        compute an n period exponential moving average.
    
        """
        prices = self.getAllPrices()
        
        x = np.asarray(prices)

        weights = np.exp(np.linspace(-1., 0., n))
    
        weights /= weights.sum()
    
        a =  np.convolve(x, weights, mode='full')[:len(x)]
        a[:n] = a[n]
        return a
    
    # from http://matplotlib.sourceforge.net/examples/pylab_examples/finance_work2.html
    def relative_strength(self, n=14):
        """
        compute the n period relative strength indicator
        http://stockcharts.com/school/doku.php?id=chart_school:glossary_r#relativestrengthindex
        http://www.investopedia.com/terms/r/rsi.asp
        """
        prices = self.getAllPrices()
        
        # find the diff between the element and the previous one
        deltas = np.diff(prices)
        seed = deltas[:n+1]
        
        # find all gains and average them
        up = seed[seed>=0].sum()/n
        
        # find all losses and average them
        down = -seed[seed<0].sum()/n
        rs = up/down
        if np.isnan(rs):
            rs = 0
        rsi = np.zeros_like(prices)
        rsi[:n] = 100. - 100./(1.+rs)
    
        for i in range(n, len(prices)):
            delta = deltas[i-1] # cause the diff is 1 shorter
    
            if delta>0:
                upval = delta
                downval = 0.
            else:
                upval = 0.
                downval = -delta
    
            up = (up*(n-1) + upval)/n
            down = (down*(n-1) + downval)/n
    
            rs = up/down
            if np.isnan(rs):
                rs = 0
            rsi[i] = 100. - 100./(1.+rs)
    
        return rsi
    
    # from http://matplotlib.sourceforge.net/examples/pylab_examples/finance_work2.html
    def moving_average_convergence(self, nslow=26, nfast=12):
        """
        compute the MACD (Moving Average Convergence/Divergence) using a fast and slow exponential moving avg'
        return value is emaslow, emafast, macd which are len(x) arrays
        """     
        emaslow = self.exponentialMovingAverage(nslow)
        emafast = self.exponentialMovingAverage(nfast)
#        return emaslow, emafast, emafast - emaslow
        return emafast - emaslow
    
    # http://docs.python.org/release/2.3.5/lib/itertools-example.html
    # chose 20 trading days because that's how many there are in a month, give or take
    def slidingWindow(self, seq, n=20):
        "Returns a sliding window (of width n) over data from the iterable"
        "   s -> (s0,s1,...s[n-1]), (s1,s2,...,sn), ...                   "
        it = iter(seq)
        result = tuple(islice(it, n))
        if len(result) == n:
            yield result    
        for elem in it:
            result = result[1:] + (elem,)
            yield result

    def setTimewindow(self, windowSize):
        self.ema = self.exponentialMovingAverage(windowSize)
        self.rsi = self.relative_strength(windowSize)
        self.macd = self.moving_average_convergence(windowSize, windowSize / 2)
        self.prices = self.getAllPrices()

    def getTimewindow(self, windowSize):
        self.setTimewindow(windowSize)
        prices = []
        ema = []
        rsi = []
        macd = []
        for window in self.slidingWindow(izip(self.prices, self.ema, self.rsi, self.macd), windowSize):
            p, e, r, m = list(izip(*window))
            # store the price for the next iteration
            prices.append(p[-1])
            ema.append(e[-1])
            rsi.append(r[-1])
            macd.append(m[-1])
        
        # get rid of the first price because there's no attributes
        prices = prices[1:]
        # slice off the first row because there's no price
        ema = ema[:-1]
        rsi = rsi[:-1]
        macd = macd[:-1]

        return prices, ema, rsi, macd
    
    def writeCsv(self, filename, prices, ema, rsi, macd):
        f = csv.writer(open(filename, 'w'))
        f.writerow(['day', 'price', 'ema', 'rsi', 'macd'])
        for i in range(len(ema)):
            f.writerow([i, prices[i], ema[i], rsi[i], macd[i]])
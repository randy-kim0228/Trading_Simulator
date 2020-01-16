"""
Implementing StrategyLearner
Name: Nam Yoon Kim
GTID: nkim84
"""

import datetime as dt
import pandas as pd
import numpy as np
import util as ut
import random
import BagLearner as bl
import RTLearner as rt
import indicators as ind

class StrategyLearner(object):

    def author(self):
        return 'nkim84'

    def __init__(self, verbose = False, impact=0.0):
        self.verbose = verbose
        self.impact = impact
        self.N = 14
        self.LONG = 1
        self.CASH = 0
        self.SHORT = -1
        self.learner = bl.BagLearner(learner = rt.RTLearner, kwargs = {"leaf_size": 5}, bags = 100, boost = False, verbose = False)

    def addEvidence(self, symbol = "IBM", \
        sd=dt.datetime(2009,1,1), \
        ed=dt.datetime(2010,1,1), \
        sv = 10000):

        # Indicators
        normed_price, sma_ratio, sma, bbp, momentum, bb = ind.indicators(sd, ed, symbol = symbol, lookback = self.N)
        indicators = pd.concat([sma, bbp['BBP'], momentum], axis = 1)
        indicators.fillna(0, inplace = True)

        # dataX & dataY for training
        dataX = indicators[:-self.N].values
        dataY = self.training_Y(normed_price, symbol = symbol)
        self.learner.addEvidence(dataX = dataX, dataY = dataY)

    def testPolicy(self, symbol = "IBM", \
        sd=dt.datetime(2009,1,1), \
        ed=dt.datetime(2010,1,1), \
        sv = 10000):

        # Indicators
        normed_price, sma_ratio, sma, bbp, momentum, bb = ind.indicators(sd, ed, symbol=symbol, lookback = self.N)
        indicators = pd.concat([sma, bbp['BBP'], momentum], axis = 1)
        indicators.fillna(0, inplace = True)

        # testX & testYx
        testX = indicators.values
        query = self.learner.query(testX)
        df_trades = pd.DataFrame(0, index = normed_price.index, columns = ['Shares'])
        share = 0

        for i in range(0, normed_price.shape[0] - self.N):
            if share == 0:
                if query[i] > 0:
                    df_trades.iloc[i]['Shares'] = 1000
                    share = 1
                elif query[i] < 0:
                    df_trades.iloc[i]['Shares'] = -1000
                    share = -1

            elif share == 1:
                if query[i] < 0:
                    df_trades.iloc[i]['Shares'] = -2000
                    share = -1
                elif query[i] == 0:
                    df_trades.iloc[i]['Shares'] = -1000
                    share = 0
            else:
                if query[i] > 0:
                    df_trades.iloc[i]['Shares'] = 2000
                    share = 1
                elif query[i] == 0:
                    df_trades.iloc[i]['Shares'] = 1000
                    share = 0
        if share == -1:
            df_trades.iloc[normed_price.shape[0] - self.N]['Shares'] = 1000

        elif share == 1:
            df_trades.iloc[normed_price.shape[0] - self.N]['Shares'] = -1000

        return df_trades

    def training_Y(self, normed_price, symbol):
        training_Y = list()
        for i in range(0, normed_price.shape[0] - self.N):
            ret = (normed_price.ix[(i + self.N), symbol] / normed_price.ix[i, symbol]) - 1
            YBUY = (self.impact + 0.02)
            YSELL = -YBUY
            if ret > YBUY:
                training_Y.append(self.LONG)
            elif ret < YSELL:
                training_Y.append(self.SHORT)
            else:
                training_Y.append(self.CASH)
        dataY = np.array(training_Y)
        return(dataY)

if __name__=="__main__":
    print "One does not simply think up a strategy"
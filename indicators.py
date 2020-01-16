"""
Implementation of Indicators
Name: Nam Yoon Kim
GTID: nkim84
"""

import pandas as pd
import datetime as dt
from util import get_data, plot_data

def author():
    return 'nkim84'

def indicators(sd = dt.datetime(2008, 1, 1), ed = dt.datetime(2009, 12, 31), symbol = 'JPM', lookback = 20):
    dates = pd.date_range(sd, ed)
    price = get_data([symbol], dates)
    if symbol != 'SPY':
        price = price.drop(['SPY'], axis=1)
    price = price[[symbol]]
    normed_price = price / price.ix[0, :]

    # 1. Simple Moving Average (SMA)
    sma = pd.DataFrame(0, index = normed_price.index, columns = ['SMA'])
    sma['SMA'] = normed_price.rolling(window = lookback).mean()
    # Calculate SMA ratio
    sma_ratio = pd.DataFrame(0, index = normed_price.index, columns = ['Price/SMA'])
    sma_ratio['Price/SMA'] = normed_price[symbol]/sma['SMA']

    # 2. Bollinger Bands (BB)
    bb = pd.DataFrame(0, index = normed_price.index, columns = ['Top', 'Bottom'])
    bands = pd.DataFrame(0, index = normed_price.index, columns = ['Band'])
    bands['Band'] = normed_price.rolling(window = lookback).std()
    bb['Top'] = sma['SMA'] + 2 * bands['Band']
    bb['Bottom'] = sma['SMA'] - 2 * bands['Band']
    # Calculate BB %
    bbp = pd.DataFrame(0, index = normed_price.index, columns = ['Price/SMA'])
    bbp['BBP'] = (normed_price[symbol] - bb['Bottom']) / (bb['Top'] - bb['Bottom'])

    # 3. Momentum
    momentum = normed_price / normed_price.shift() - 1
    momentum = pd.DataFrame(data= momentum.ix[:, 0])

    return normed_price, sma_ratio, sma, bbp, momentum, bb
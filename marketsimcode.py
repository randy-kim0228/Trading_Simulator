"""
Implementation marketsimcode
Name: Nam Yoon Kim
GTID: nkim84
"""

import pandas as pd
import numpy as np
import datetime as dt
import os
from util import get_data, plot_data

def author():
    return 'nkim84'

def compute_portvals(orders, start_val = 1000000, commission=9.95, impact=0.005):
    # this is the function the autograder will call to test your code
    # NOTE: orders_file may be a string, or it may be a file object. Your
    # code should work correctly with either input
    # TODO: Your code here
    # Step 1: Prices
    df_orders = orders
    df_orders = df_orders.sort_index()
    start_date = df_orders.index.min()
    end_date = df_orders.index.max()
    symbols = df_orders.Symbol.unique().tolist()

    # creating data frame including closing prices of ranged date
    df_prices = get_data(symbols, pd.date_range(start_date, end_date))
    df_prices = df_prices.drop('SPY', axis = 1)
    df_prices['CASH'] = 1

    # Step 2: Trades
    df_trades = df_prices.copy()
    df_trades[:] = 0
    for index, row in df_orders.iterrows():
        symbols = row['Symbol']
        orders = row['Order']
        shares = row['Shares']
        if orders == 'BUY':
            df_trades.ix[index, symbols] += shares
            df_trades.ix[index, 'CASH'] -= df_prices.ix[index, symbols] * shares * (1 + impact) + commission
        else:
            df_trades.ix[index, symbols] -= shares
            df_trades.ix[index, 'CASH'] += df_prices.ix[index, symbols] * shares * (1 - impact) - commission

    # Step 3: Holdings
    df_holdings = df_prices.copy()
    df_holdings[:] = 0
    df_holdings.loc[start_date, 'CASH'] = start_val
    df_holdings.ix[0] += df_trades.ix[0]
    for i in range(1, len(df_trades)):
        df_holdings.ix[i] += df_trades.ix[i] + df_holdings.ix[i - 1]

    # Step 4: Values
    df_values = df_prices * df_holdings
    port_val = df_values.sum(axis = 1)
    return port_val

# Functions from 'assess_portfolio' for examples to check the code
def portfolio_values(prices, allocs, sv = 1):
    normed = prices / prices.ix[0,:]
    alloced = normed * allocs
    pos_vals = alloced * sv
    portfolio_val = pos_vals.sum(axis=1)
    return portfolio_val

def portfolio_stats(portfolio_val, rfr=0.0, sf=252.0):
    daily_returns = portfolio_val.copy()
    daily_returns[1:] = (daily_returns[1:] / daily_returns[:-1].values) - 1
    daily_returns.ix[0] = 0
    cr = (portfolio_val[-1] / portfolio_val[0]) - 1
    adr = daily_returns[1:].mean()
    sddr = daily_returns[1:].std()
    sr = np.sqrt(sf) * (adr - rfr) / sddr
    return cr, adr, sddr, sr

def test_code():
    # this is a helper function you can use to test your code
    # note that during autograding this function will not be called.
    # Define input parameters

    of = "./Additional_orders/additional_orders/orders-short.csv"
    # of = "./Additional_orders/additional_orders/orders.csv"
    # of = "./Additional_orders/additional_orders/orders2.csv"
    sv = 1000000

    # Process orders
    portvals = compute_portvals(orders_file = of, start_val = sv)
    if isinstance(portvals, pd.DataFrame):
        portvals = portvals[portvals.columns[0]] # just get the first column
    else:
        "warning, code did not return a DataFrame"

    # Short example to check code
    df_orders = pd.read_csv(of, index_col = 'Date', parse_dates = True, na_values = ['nan'])
    df_orders = df_orders.sort_index()
    start_date = df_orders.index.min()
    end_date = df_orders.index.max()
    df_prices = get_data(['$SPX'], pd.date_range(start_date, end_date))
    df_prices = df_prices[['$SPX']]
    df_prices_aapl = get_data(['AAPL'], pd.date_range(start_date, end_date))
    df_prices_aapl = df_prices_aapl[['AAPL']]
    port_val_SPX = portfolio_values(df_prices, [1.0])
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = portfolio_stats(portvals)
    cum_ret_SPX, avg_daily_ret_SPX, std_daily_ret_SPX, sharpe_ratio_SPX = portfolio_stats(port_val_SPX)

    # Compare portfolio against $SPX
    print "SHORT EXAMPLE TO CHECK THE CODE"
    print
    print "The Daily Value of Portfolio: \n{}".format(portvals.to_string(header = None))
    print
    print "The Adjusted Close Values for AAPL on the relevant days: \n{}".format(df_prices_aapl)
    print
    print "The Full Results:"
    print
    print "Date Range: {} to {}".format(start_date, end_date)
    print
    print "Sharpe Ratio of Fund: {}".format(sharpe_ratio)
    print "Sharpe Ratio of $SPX : {}".format(sharpe_ratio_SPX)
    print
    print "Cumulative Return of Fund: {}".format(cum_ret)
    print "Cumulative Return of $SPX : {}".format(cum_ret_SPX)
    print
    print "Standard Deviation of Fund: {}".format(std_daily_ret)
    print "Standard Deviation of $SPX : {}".format(std_daily_ret_SPX)
    print
    print "Average Daily Return of Fund: {}".format(avg_daily_ret)
    print "Average Daily Return of $SPX : {}".format(avg_daily_ret_SPX)
    print
    print "Final Portfolio Value: {}".format(portvals[-1])

if __name__ == "__main__":
    test_code()
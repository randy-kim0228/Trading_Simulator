"""
Experiment 1
Name: Nam Yoon Kim
GTID: nkim84
"""

import datetime as dt
import numpy as np
import random
import pandas as pd
import marketsimcode as ms
import util as ut
import StrategyLearner as sl
import matplotlib.pyplot as plt
import indicators as ind

def author():
    return 'nkim84'

if __name__ == "__main__":
    seed = 1481090000
    np.random.seed(seed)
    random.seed(seed)

    sv = 100000
    learner = sl.StrategyLearner(verbose = False, impact = 0.0)
    learner.addEvidence(symbol = 'JPM')
    sl_trade = learner.testPolicy(symbol = 'JPM', sd = dt.datetime(2008, 1, 1), ed = dt.datetime(2009, 12, 31), sv = sv)

    sl_trade['Symbol'] = 'JPM'
    sl_trade['Order'] = 'BUY'
    sl_trade.loc[sl_trade.Shares < 0, 'Order'] = 'SELL'
    sl_trade = sl_trade[sl_trade.Shares != 0]
    sl_trade.Shares = abs(sl_trade.Shares)
    sl_trade = sl_trade[['Symbol', 'Order', 'Shares']]

    sl = ms.compute_portvals(sl_trade, start_val = sv, commission = 0, impact = 0)

    syms = ['JPM']
    dates = pd.date_range(dt.datetime(2008, 1, 1), dt.datetime(2009, 12, 31))
    prices_all = ut.get_data(syms, dates)  # automatically adds SPY
    prices_JPM = prices_all['JPM']  # only SPY, for comparison later

    share = [1000, -1000]
    date = [prices_all.index[0], prices_all.index[len(prices_all.index) - 1]]
    benchmark = pd.DataFrame(data = share, index = date, columns = ['Shares']) # call out first and last row of JPM
    benchmark['Symbol'] = 'JPM'
    benchmark['Order'] = 'BUY'
    benchmark.loc[benchmark.Shares < 0, 'Order'] = 'SELL'
    benchmark = benchmark[['Symbol', 'Order', 'Shares']]
    bm = ms.compute_portvals(benchmark, start_val = sv, commission=0, impact=0)

    sl_normed = sl / sl[0]
    bm_normed = bm / bm[0]

    # Plot for STRATEGY vs BENCHMARK
    plot_df = pd.concat([sl_normed, bm_normed], axis = 1)
    plot_df.columns = ['Strategy', 'Benchmark']
    plot_df.plot(title = 'Experiment 1', use_index = True, color = ['Blue', 'Black'])
    plt.xlabel('Date')
    plt.ylabel('Portfolio (Normed)')
    plt.show()

    sl_cr, sl_adr, sl_sddr, sl_sr = ms.portfolio_stats(sl)
    print(sl_cr, sl_adr, sl_sddr, sl_sr)
    bm_cr, bm_adr, bm_sddr, bm_sr = ms.portfolio_stats(bm)
    print(bm_cr, bm_adr, bm_sddr, bm_sr)
    # # Indicators_overall Plot
    # normed_price, sma, bbp, momentum, bb = ind.indicators(sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31),
    #                                                       symbol='JPM', lookback=14)
    # plot_indicators = pd.concat([normed_price, sma['SMA'], bb['Top'], bb['Bottom'], momentum], axis=1)
    # plot_indicators.columns = ['Normed Price', 'Rolling Mean (SMA)', 'Upper Band (BB)', 'Lower Band (BB)', 'Momentum']
    # plot_indicators.plot(title='Indicators', use_index=True, color=['Red', 'Green', 'Blue', 'Grey', 'Black'])
    # plt.xlabel('Date')
    # plt.ylabel('Portfolio (Normed)')
    # plt.legend(loc=5, prop={'size': 6})
    # plt.show()

    # Indicators Plot
    # normed_price, sma_ratio, sma, bbp, momentum, bb = ind.indicators(sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31),
    #                                                       symbol='JPM', lookback=14)
    # plot_indicators = pd.concat([normed_price, sma['SMA'], sma_ratio['Price/SMA']], axis=1)
    # plot_indicators.columns = ['Normed Price', 'Rolling Mean (SMA)', 'Price/SMA']
    # plot_indicators.plot(title='Indicators', use_index=True, color=['Red', 'Green', 'Blue'])
    # plt.xlabel('Date')
    # plt.ylabel('Portfolio (Normed)')
    # plt.legend(loc=4, prop={'size': 8})
    # plt.show()
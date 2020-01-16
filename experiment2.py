"""
Experiment 2
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

def author():
    return 'nkim84'

if __name__ == "__main__":
    seed = 1481090000
    np.random.seed(seed)
    random.seed(seed)

    sv = 100000
    learner1 = sl.StrategyLearner(verbose = False, impact = 0.00001)
    learner1.addEvidence(symbol = 'JPM')
    sl_trade1 = learner1.testPolicy(symbol ='JPM', sd = dt.datetime(2008, 1, 1), ed = dt.datetime(2009, 12, 31), sv = sv)
    sl_trade1['Symbol'] = 'JPM'
    sl_trade1['Order'] = 'BUY'
    sl_trade1.loc[sl_trade1.Shares < 0, 'Order'] = 'SELL'
    sl_trade1 = sl_trade1[sl_trade1.Shares != 0]
    sl_trade1.Shares = abs(sl_trade1.Shares)
    sl_trade1 = sl_trade1[['Symbol', 'Order', 'Shares']]

    learner2 = sl.StrategyLearner(verbose = False, impact = 0.0001)
    learner2.addEvidence(symbol = 'JPM')
    sl_trade2 = learner2.testPolicy(symbol = 'JPM', sd = dt.datetime(2008, 1, 1), ed = dt.datetime(2009, 12, 31), sv = sv)
    sl_trade2['Symbol'] = 'JPM'
    sl_trade2['Order'] = 'BUY'
    sl_trade2.loc[sl_trade2.Shares < 0, 'Order'] = 'SELL'
    sl_trade2 = sl_trade2[sl_trade2.Shares != 0]
    sl_trade2.Shares = abs(sl_trade2.Shares)
    sl_trade2 = sl_trade2[['Symbol', 'Order', 'Shares']]

    learner3 = sl.StrategyLearner(verbose = False, impact = 0.001)
    learner3.addEvidence(symbol = 'JPM')
    sl_trade3 = learner3.testPolicy(symbol = 'JPM', sd = dt.datetime(2008, 1, 1), ed = dt.datetime(2009, 12, 31), sv = sv)
    sl_trade3['Symbol'] = 'JPM'
    sl_trade3['Order'] = 'BUY'
    sl_trade3.loc[sl_trade3.Shares < 0, 'Order'] = 'SELL'
    sl_trade3 = sl_trade3[sl_trade3.Shares != 0]
    sl_trade3.Shares = abs(sl_trade3.Shares)
    sl_trade3 = sl_trade3[['Symbol', 'Order', 'Shares']]

    sl_impact1 = ms.compute_portvals(sl_trade1, start_val = sv, commission = 0, impact = 0.00001)
    sl_impact2 = ms.compute_portvals(sl_trade2, start_val = sv, commission = 0, impact = 0.0001)
    sl_impact3 = ms.compute_portvals(sl_trade3, start_val = sv, commission = 0, impact = 0.001)
    sl_impact1_normed = sl_impact1 / sl_impact1[0]
    sl_impact2_normed = sl_impact2 / sl_impact2[0]
    sl_impact3_normed = sl_impact3 / sl_impact3[0]

    plot_df = pd.concat([sl_impact1_normed, sl_impact2_normed, sl_impact3_normed], axis = 1)
    plot_df.columns = ['SL(Impact = 0.00001)', 'SL(Impact = 0.0001)', 'SL(Impact = 0.001)']
    plot_df.plot(title='Experiment 2', use_index=True, color=['Red', 'Green', 'Blue'])
    plt.xlabel('Date')
    plt.ylabel('Portfolio(Normed)')
    plt.show()

    sl1_cr, sl1_adr, sl1_sddr, sl1_sr = ms.portfolio_stats(sl_impact1_normed)
    print(sl1_cr, sl1_adr, sl1_sddr, sl1_sr)
    sl2_cr, sl2_adr, sl2_sddr, sl2_sr = ms.portfolio_stats(sl_impact2_normed)
    print(sl2_cr, sl2_adr, sl2_sddr, sl2_sr)
    sl3_cr, sl3_adr, sl3_sddr, sl3_sr = ms.portfolio_stats(sl_impact3_normed)
    print(sl3_cr, sl3_adr, sl3_sddr, sl3_sr)
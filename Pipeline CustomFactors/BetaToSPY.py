import pandas as pd
import numpy as np

def _beta(ts, benchmark, benchmark_var):
    return np.cov(ts, benchmark)[0, 1] / benchmark_var

class BetaToSpy(CustomFactor):
    # James Christopher
    # https://www.quantopian.com/posts/pipeline-calculating-beta
    #
    inputs = [USEquityPricing.close]
    window_length = 60

    def compute(self, today, assets, out, close):
        returns = pd.DataFrame(close, columns=assets).pct_change()[1:]
        spy_returns = returns[sid(8554)]
        spy_returns_var = np.var(spy_returns)
        out[:] = returns.apply(_beta, args=(spy_returns,spy_returns_var,))

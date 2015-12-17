import numpy as np

class AvgDailyDollarVolumeTraded(CustomFactor):
    # John Fawcett
    # https://www.quantopian.com/posts/dollar-volume-pipeline
    #
    inputs = [USEquityPricing.close, USEquityPricing.volume]
    def compute(self, today, assets, out, close_price, volume):
        dollar_volume = close_price * volume
        avg_dollar_volume = np.mean(dollar_volume, axis=0)
        out[:] = avg_dollar_volume

import numpy as np

class ParkinsonVolatility(CustomFactor):
    # Jason
    # https://www.quantopian.com/posts/using-pipeline-with-customfactor
    #
    inputs = [USEquityPricing.high, USEquityPricing.low]

    def compute(self, today, assets, out, high, low):
        # high and low are data frames with window_lengh rows of data
        # http://www.ivolatility.com/help/3.html
        x = np.log(high/low)

        rs = (1.0/(4.0*math.log(2.0)))*x**2

        p_vol = np.sqrt(rs.mean(axis=0))

        out[:] = p_vol

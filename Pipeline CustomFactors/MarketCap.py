class MarketCap(CustomFactor):

    # Pre-declare inputs and window_length
    inputs = [USEquityPricing.close, morningstar.valuation.shares_outstanding]
    window_length = 1

    # Compute market cap value
    def compute(self, today, assets, out, close, shares):
        out[:] = close[-1] * shares[-1]

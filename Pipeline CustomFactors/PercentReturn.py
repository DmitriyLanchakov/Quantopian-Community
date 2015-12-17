class PercentReturn(CustomFactor):
    #
    # https://www.quantopian.com/posts/pipeline-mean-reversion-example
    #
    # Set the default list of inputs as well as the default window_length.
    # Default values are used if the optional parameters are not specified.
    inputs = [USEquityPricing.close]
    window_length = 10

    # Computes the returns over the last n days where n = window_length.
    # Any calculation can be performed here and is applied to all stocks
    # in the universe.
    def compute(self, today, assets, out, close):
        out[:] = (close[-1] - close[0]) / close[0]

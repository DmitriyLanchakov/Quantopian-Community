class PercentChange(CustomFactor):
    # Tristan Rhodes
    # https://www.quantopian.com/posts/my-first-pipeline-how-to-find-stocks-with-consecutive-higher-lows-low-4-low-3-low-2-low-1
    #
    # PercentChange will calculate the percent change of an input over the n-most recent days, where n = window_length.
    # This can by used for price inputs (low, high, close, open), volume, or even fundamentals (set window length for desired period)

    # Set the default list of inputs as well as the default window_length.
    # Default values are used if the optional parameters are not specified.
    inputs = [USEquityPricing.close]
    window_length = 10

    def compute(self, today, assets, out, input1):
        out[:] = (input1[-1] - input1[0]) / input1[0]

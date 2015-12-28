class ConsecutiveHigherValues(CustomFactor):
    # Tristan Rhodes
    # https://www.quantopian.com/posts/my-first-pipeline-how-to-find-stocks-with-consecutive-higher-lows-low-4-low-3-low-2-low-1
    #
    # ConsecutiveHigherValues will return the number of periods that the input has consecutively increased, leading up to the current period.
    # This can by used for price inputs (low, high, close, open) or volume.  (Fundamentals don't usually change on a daily basis, right?)
    #
    # Set the default list of inputs as well as the default window_length.
    # Default values are used if the optional parameters are not specified.
    window_length = 10
    inputs = [USEquityPricing.low]

    def compute(self, today, assets, out, input1):
        for a in range(len(assets)):
            consecutive = 0
            for i in range(-1,-self.window_length,-1):
                if input1[i-1,a] < input1[i,a]:
                    consecutive = abs(i)
                else:
                    break
            out[a] = consecutive

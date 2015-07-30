def time_since_price_was_higher(price_data):  
    # Create a series that only includes periods when the price was higher than now
    highers = price_data[price_data > price_data[-1]]
	# Save the current datetime
    now = price_data.index[-1]
	# Save the datetime of the most recent high
    last_higher = highers.index[-1]
	# Return a time delta since the previous high
    return now - last_higher
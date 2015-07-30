def time_since_price_was_lower(price_data):  
    # Create a series that only includes periods when the price was lower than now
    lowers = price_data[price_data < price_data[-1]]  
    # Save the current datetime
    now = price_data.index[-1]  
    # Save the datetime of the most recent low
    last_lower = lowers.index[-1]  
    # Return a time delta since the previous low
    return now - last_lower
def time_since_price_was_higher(price_data):  
    highers = price_data[price_data > price_data[-1]]  
    today = price_data.index[-1]  
    last_higher = highers.index[-1]  
    return today - last_higher  
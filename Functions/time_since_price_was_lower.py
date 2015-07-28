def time_since_price_was_lower(price_data):  
    lowers = price_data[price_data < price_data[-1]]  
    today = price_data.index[-1]  
    last_lower = highers.index[-1]  
    return today - last_lower  
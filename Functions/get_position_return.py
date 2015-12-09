def get_position_return(context, stock):
    # Return the percentage gain (or loss) of a position
	# Example:
	#     Cost = 10
	#     Price = 12
	#     Gain = 0.20
    if s in context.portfolio.positions:
        cost =   context.portfolio.positions[stock].cost_basis
        amount = context.portfolio.positions[stock].amount 
        price =  context.portfolio.positions[stock].last_sale_price
        if amount > 0:
            gain = price/cost - 1        
        if amount < 0:
            gain = 1 - price/cost
    else:
        gain = 0
    return gain 
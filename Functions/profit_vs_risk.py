# 
#
# garyha
# https://www.quantopian.com/posts/a-carry-strategy-with-portfolio-optimization#567bca2f0ac0cca3d100001b

def initialize(context):

    # for profit_vs_risk()
    c = context
    c.max_lvrg = 0
    c.risk_hi  = 0
    c.date_prv = ''
    c.cash_low = c.portfolio.starting_cash
    c.date_end = str(get_environment('end').date())
    log.info('{} to {}  {}  {}'.format(str(get_datetime().date()), c.date_end,
        int(c.cash_low), get_environment('data_frequency')))

def handle_data(context, data):
    # Run profit_vs_risk every minute
    profit_vs_risk(context, data)

def profit_vs_risk(context, data):
    ''' Custom chart and/or log of profit_vs_risk returns and related information
    '''
    # # # # # # # # # #  Options  # # # # # # # # # #
    record_max_lvrg = 1          # Maximum leverage encountered
    record_leverage = 0          # Leverage (context.account.leverage)
    record_q_return = 0          # Quantopian returns (percentage)
    record_profit_vs_risk      = 1          # Profit vs Risk returns (percentage)
    record_pnl      = 0          # Profit-n-Loss
    record_shorting = 1          # Total value of any shorts
    record_risk     = 0          # Risked, maximum cash spent or shorts in excess of cash at any time
    record_risk_hi  = 1          # Highest risk overall
    record_cash     = 0          # Cash available
    record_cash_low = 1          # Any new lowest cash level
    logging         = 1          # Also log to the logging window conditionally (1) or not (0)
    log_method      = 'risk_hi'  # 'daily' or 'risk_hi'

    c = context                          # For brevity
    new_cash_low = 0                     # To trigger logging in cash_low case
    date = str(get_datetime().date())    # To trigger logging in daily case
    cash = c.portfolio.cash

    if int(cash) < c.cash_low:    # New cash low
        new_cash_low = 1
        c.cash_low   = int(cash)
        if record_cash_low:
            record(CashLow = int(c.cash_low))

    profit_vs_risk_rtrn      = 0        # Profit vs Risk returns based on maximum spent
    profit_loss   = 0        # Profit-n-loss
    shorts        = 0        # Shorts value
    start         = c.portfolio.starting_cash
    cash_dip      = int(max(0, start - cash))

    if record_cash:
        record(Cash = int(c.portfolio.cash))  # Cash

    if record_leverage:
        record(Lvrg = c.account.leverage)     # Leverage

    if record_max_lvrg:
        if c.account.leverage > c.max_lvrg:
            c.max_lvrg = c.account.leverage
            record(MaxLv = c.max_lvrg)        # Maximum leverage

    if record_pnl:
        profit_loss = c.portfolio.pnl
        record(PnL = profit_loss)             # "Profit and Loss" in dollars

    for p in c.portfolio.positions:
        shrs = c.portfolio.positions[p].amount
        if shrs < 0:
            shorts += int(abs(shrs * data[p].price))

    if record_shorting:
        record(Shorts = shorts)               # Shorts value as a positve

    risk = int(max(cash_dip, shorts))
    if record_risk:
        record(Risk = risk)                   # Amount in play, maximum of shorts or cash used

    new_risk_hi = 0
    if risk > c.risk_hi:
        c.risk_hi = risk
        new_risk_hi = 1

        if record_risk_hi:
            record(RiskHi = c.risk_hi)        # Highest risk overall

    if record_profit_vs_risk:      # Profit_vs_Risk returns based on max amount actually spent (risk high)
        if c.risk_hi != 0:     # Avoid zero-divide
            profit_vs_risk_rtrn = 100 * (c.portfolio.portfolio_value - start) / c.risk_hi
            record(profit_vs_risk = profit_vs_risk_rtrn)            # Profit_vs_Risk returns

    q_rtrn = 100 * (c.portfolio.portfolio_value - start) / start
    if record_q_return:
        record(QRet = q_rtrn)                 # Quantopian returns to compare to profit_vs_risk returns curve

    from pytz import timezone
    if logging:
        if log_method == 'risk_hi' and new_risk_hi \
          or log_method == 'daily' and c.date_prv != date \
          or c.date_end == date \
          or new_cash_low:
            qret   = 'QRet '    + '%.1f' % q_rtrn
            mxlv   = 'MaxLv '   + '%.1f' % c.max_lvrg   if record_max_lvrg else ''
            profit_vs_risk    = 'profit_vs_risk '     + '%.1f' % profit_vs_risk_rtrn     if record_profit_vs_risk      else ''
            pnl    = 'PnL '     + '%.0f' % profit_loss  if record_pnl      else ''
            csh    = 'Cash '    + '%.0f' % cash         if record_cash     else ''
            csh_lw = 'CshLw '   + '%.0f' % c.cash_low   if record_cash_low else ''
            shrt   = 'Shrt '    + '%.0f' % shorts       if record_shorting else ''
            risk   = 'Risk '    + '%.0f' % risk         if record_risk     else ''
            rsk_hi = 'RskHi '   + '%.0f' % c.risk_hi    if record_risk_hi  else ''
            minute = get_datetime().astimezone(timezone('US/Eastern')).time().minute
            log.info('{} {} {} {} {} {} {} {} {} {}'.format(
                    minute, mxlv, qret, profit_vs_risk, pnl, csh, csh_lw, shrt, risk, rsk_hi))

    if c.date_end == date:    # Log on last day, like cash 125199  portfolio 126890
        log.info('cash {}  portfolio {}'.format(
                int(cash), int(c.portfolio.portfolio_value)))

    c.date_prv = date

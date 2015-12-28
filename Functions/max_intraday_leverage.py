# garyha
# https://www.quantopian.com/posts/maximum-leverage-charting-not-just-leverage-star-important-star

def initialize(context):

    context.lvrg_max_intraday = 0    # A variable to keep track of highest leverage seen each day.
    schedule_function(max_intraday_leverage_record, date_rules.every_day(), time_rules.market_close())

def max_intraday_leverage(c):
    ''' Record maximum leverage reached throughout any day, for minute mode.
        Input context is set to 'c' for better readability.
    '''
    if c.account.leverage > c.lvrg_max_intraday:
        c.lvrg_max_intraday = c.account.leverage

    record(end_of_day_leverage = c.account.leverage)  # Will only be the last one of the day

    # To examine a date
    examine_date = ''    # Empty for off, or fill this with like '2013-07-19' to activate
    if examine_date and str(get_datetime().date()) == examine_date:
        from pytz import timezone    # Python will only bother doing this once, makes this portable.
        bar_dt = get_datetime().astimezone(timezone('US/Eastern'))        # Set to Eastern
        minute = (bar_dt.hour * 60) + bar_dt.minute - 570  # (-570 = 9:31a) Trading minute 1 to 390
        log.info('{} {} {} '.format(minute, '%.6f' % c.account.leverage, '%.6f' % c.lvrg_max_intraday))

def max_intraday_leverage_record(context, data):
    # On last minute of the day, record maximum leverage encountered throughout this day.
    record(lvrg_day_max = context.lvrg_max_intraday)
    context.lvrg_max_intraday = 0             #   Then reset, start fresh next day.

def handle_data(context, data):
    max_intraday_leverage(context)    # Call function for recording maximum leverage of the day
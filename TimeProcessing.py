import MetaTrader5 as mt5 
from pytz import utc 
from datetime import datetime, time  


def MarketIsOpen():
    '''This function adjusts the bot's working to the forex market working hours (UTC time).'''

    #Adjusting bot working hours according to UTC time
    date_now = datetime.now(tz=utc)
    time_now = date_now.time()
    open_time, close_time = time(hour=22, minute=00, second=00), time(hour=21, minute=59, second=00)
    if date_now.weekday() != 5:
        if date_now.weekday() == 6 and time_now < open_time:
            return False
        elif date_now.weekday() == 4 and time_now >= close_time:
            return False
        else:
            return True
    else:
        return False

def NewCandleUpdate(tframe: str, CandlesRetrieved: int):
    '''
    Returns True if a new candle starts or emerges based on the given trading timeframe (tframe); 
    otherwise, returns False. By signalling to the program the start of a new candle, the program 
    engages in a new loop, analyzing and applying the indicator measures to the new data.\n\n
    Also, if CandlesRetrieved is True, it returns False, preventing the program from analyzing the
    same candle twice.\n 

    **Note, the function is adjusted to UTC time to track MT5 candle update times.**\n\n

    Valid time inputs are:
           [5m, 15m, 30m, 1h, 2h, 3h, 4h, 1d]    
    '''

    if CandlesRetrieved is True:
        return False    
        
    if tframe == '5m':
        return (True if (datetime.now().minute % 5 == 0) else False)
    elif tframe == '15m':
        return (True if (datetime.now().minute % 15 == 0) else False)
    elif tframe == '30m':
        return (True if (datetime.now().minute % 30 == 0) else False)
    elif tframe == '1h':
        return (True if (datetime.now().minute == 0) else False)
    elif tframe == '2h':
        return (True if ((datetime.now(tz=utc).hour % 2 == 0) and (datetime.now().minute == 0)) else False)
    elif tframe == '3h':
        return (True if ((datetime.now(tz=utc).hour % 3 == 0) and (datetime.now().minute == 0)) else False)
    elif tframe == '4h': 
        return (True if ((datetime.now(tz=utc).hour % 4 == 0) and (datetime.now().minute == 0)) else False)
    elif tframe == '1d':
        return (True if ((datetime.now(tz=utc).hour == 0) and (datetime.now().minute == 0)) else False)
    else:
        print('Invalid time. Re-enter a timeframe from the list.')
        return None

def get_mt5_interval(trading_frame):
    '''
    #### Returns MT5 timeframe object corresponding to the given trading timeframe.

    #### Valid timeframe inputs are:
    ####        [1m, 5m, 15m, 30m, 1h, 2h, 3h, 4h, 1d]      '''

    if trading_frame == '1m':
        return mt5.TIMEFRAME_M1
    if trading_frame == '5m':
        return mt5.TIMEFRAME_M5
    elif trading_frame == '15m':
        return mt5.TIMEFRAME_M15
    elif trading_frame == '30m':
        return mt5.TIMEFRAME_M30
    elif trading_frame == '1h':
        return mt5.TIMEFRAME_H1
    elif trading_frame == '2h':
        return mt5.TIMEFRAME_H2
    elif trading_frame == '3h':
        return mt5.TIMEFRAME_H3
    elif trading_frame == '4h':
        return mt5.TIMEFRAME_H4
    elif trading_frame == '1d':
        return mt5.TIMEFRAME_D1
    else:
        return None


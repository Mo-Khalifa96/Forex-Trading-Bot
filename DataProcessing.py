import numpy as np 
import pandas as pd 
from talib import ATR
from backtesting.lib import cross


def nz(x, y=None):
    if x is np.nan or x is None:
        if y is not None and y is not np.nan:
            return y
        else:
            return 0
    else:
        return x

def Cross(dfclose, sptlist):
    if cross(dfclose[-len(sptlist):], pd.Series(sptlist)):
        return True 
    else:
        return False 

def Indicator(df_rates_orig: pd.DataFrame):
    '''
    This function takes a dataframe with the candlesticks for a given symbol, applies the indicator or trading strategy 
    analysis, and returns back 3 key indicator variables:
            maximum: the indicator's green line,
            average: the indicator's orange line, &
            minimum: the indicator's red line. \n
    
    **Note, it processes up to next to last candle only.**
                                                           '''

    # Define empty lists for indicator variables 
    upper_lst, lower_lst, spt_lst, os_lst, max_lst, min_lst = [np.nan], [np.nan], [np.nan], [np.nan], [np.nan], [np.nan]

    #Preprocessing to prepare the variable lists!
    i = -500
    while i < 0:
        #Get the data to build the lists
        df = df_rates_orig[:i] 
        src = df['close'].iloc[-1]
        current_atr18 = ATR(high= df['high'], low=df['low'], close=df['close'], timeperiod=18).iloc[-1]
        atr = current_atr18 * 5
        up, dn = np.mean([df['high'].iloc[-1], df['low'].iloc[-1]]) + atr, np.mean([df['high'].iloc[-1], df['low'].iloc[-1]]) - atr

        #get upper
        if df['close'].iloc[-2] < upper_lst[-1]:
            upper = min(up, upper_lst[-1])
        else:
            upper = up

        # get lower
        if df['close'].iloc[-2] > lower_lst[-1]:
            lower = max(dn, lower_lst[-1])
        else:
            lower = dn

        #get os
        if src > upper:
            os = 1
        elif src < lower:
            os = 0
        else:
            os = os_lst[-1]

        #get spt
        if os == 1:
            spt = lower
        else:
            spt = upper

        #get maximum and minimum
        if Cross(df['close'], spt_lst):
            max_val, min_val = nz(max(max_lst[-1], src), src), nz(min(min_lst[-1], src), src)
        elif os == 0:
            max_val, min_val = min(spt, max_lst[-1]), min(src, min_lst[-1])
        else:
            max_val, min_val = max(src, max_lst[-1]), max(spt, min_lst[-1])

        #get average
        avg_val = np.mean([max_val, min_val])

        #Append new values 
        upper_lst.append(upper), lower_lst.append(lower), os_lst.append(os), spt_lst.append(spt), max_lst.append(max_val), min_lst.append(min_val)

        #add 1
        i += 1

    return max_val, min_val, avg_val



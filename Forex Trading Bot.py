import sys 
import pandas as pd 
from time import sleep
import MetaTrader5 as mt5 
from datetime import datetime
from DataProcessing import Indicator
from OrderProcessing import Execute_Buy_Order, Execute_Sell_Order
from TimeProcessing import MarketIsOpen, NewCandleUpdate, get_mt5_interval



#Trading symbols and timeframes 
symbols = (['EURUSD', '15m', False], ['EURGBP', '15m', False], ['EURCAD', '15m', False], ['EURAUD', '15m', False], ['EURNZD', '15m', False], 
['EURCHF', '30m', False], ['GBPUSD', '30m', False], ['GBPCAD', '30m', False], ['GBPNZD', '30m', False], ['GBPAUD', '30m', False], 
['GBPJPY', '1h', False], ['GBPCHF', '1h', False], ['USDCAD', '1h', False], ['USDJPY', '1h', False], ['USDCHF', '1h', False], 
['CADJPY', '2h', False], ['CADCHF', '2h', False], ['NZDUSD', '2h', False], ['NZDCAD', '2h', False], ['NZDCHF', '2h', False], 
['AUDUSD', '4h', False], ['AUDCAD', '4h', False], ['AUDNZD', '4h', False], ['AUDJPY', '4h', False], ['AUDCHF', '4h', False], 
['CHFJPY', '4h', False])

#Symbols Attributes:
#symbol, timeframe, CandlesRetrieved = symbol_lst[0], symbol_lst[1], symbol_lst[2]


#First Loop: Program Loop
while True:
    #Check market time and connect to MT5 
    if not MarketIsOpen():
        for symbol_lst in symbols: 
            symbol_lst[2] = False
        
        #Connect to MetaTrader5 and login to personal account
        #Get account details 
        while True:
            try:
                mt5_account, mt5_passw, server = int(input('Enter MT5 account number: ')), str(input('Enter MT5 password: ')), str(input('Enter server name: '))
                break 
            except:
                print('Invalid input. Please try again.')
                
        #Initialize MetaTrader5 terminal
        if not mt5.initialize(login=mt5_account, password=mt5_passw, server=server):
            print(f'initialize() failed, error code={mt5.last_error()}')
            sys.exit()

        #Logging in to MT5 account 
        if not mt5.login(login=mt5_account, password=mt5_passw, server=server):
            print(f'Failed to connect to account #{mt5_account}, error code={mt5.last_error()}')
            mt5.shutdown()
            sys.exit()

    else:
        continue


    #Second Loop: Analysis & Trading Loop
    while True:
        #Check internet connection from terminal
        if not mt5.terminal_info().connected:
            continue 

        for symbol_lst in symbols:
            #Check if current symbol has new candles 
            if NewCandleUpdate(symbol_lst[1], symbol_lst[2]):
                #Select symbol on Market Watch
                if not mt5.symbol_select(symbol_lst[0]):
                    print(f'Failed to select {symbol_lst[0]} on Market Watch, error code={mt5.last_error()}\nShutting down the program...')
                    mt5.shutdown()
                    sys.exit()
                    
                #Process candles only if symbol has no open positions 
                if len(mt5.positions_get(symbol=symbol_lst[0])) < 1:
                    #Get rates for current symbol (retrieve last 550 candles)
                    rates = mt5.copy_rates_from_pos(symbol_lst[0], get_mt5_interval(symbol_lst[1]), 0, 550)
                    if rates is not None:
                        #Create DataFrame out of the obtained data
                        df_rates = pd.DataFrame(rates)
                        #Get current open and previous high and low prices 
                        curr_open, prv_high, prv_low = df_rates.iloc[-1][1], df_rates.iloc[-2][2], df_rates.iloc[-2][3]
                    else:
                        print(f'Failed to retrieve rates for {symbol_lst[0]} from MT5 terminal. Trying again...')
                        break    #breaks for loop and restarts second while loop again...
                        

                    #Analyze candles and return indicator lines values for previous candle
                    maximum, minimum, average = Indicator(df_rates)
                    
                    
                    #Define buy and sell Conditions 
                    buy_condition = ((prv_low <= minimum) and (curr_open < average))
                    sell_condition =  ((prv_high >= maximum) and (curr_open > average))

                    #Execute Sell/Buy Order if conditions are met
                    if buy_condition:
                        Execute_Buy_Order(symbol=symbol_lst[0], openp=curr_open, min_val=minimum, avg_val=average)
                    elif sell_condition:
                        Execute_Sell_Order(symbol=symbol_lst[0], openp=curr_open, max_val=maximum, avg_val=average)

            #To prevent processing same candle twice, set CandlesRetrieved as True/False
            curr_candle_t = datetime.fromtimestamp(mt5.copy_rates_from_pos(symbol_lst[0], get_mt5_interval(symbol_lst[1]), 0, 1)[0][0])
            symbol_lst[2] = True if ((curr_candle_t.minute ==  datetime.now().minute) and (curr_candle_t.hour ==  datetime.now().hour)) else False
                
        #FOR LOOP ENDS
        #Check if market still open...
        if not MarketIsOpen():
            print('\nMARKET CLOSING SOON.\nSleeping till Sunday 09:59:00 PM...')
            sleep(172800)    #sleep for 48 hours
            break  # breaks the while loop above (Analysis & Trading Loop)
    


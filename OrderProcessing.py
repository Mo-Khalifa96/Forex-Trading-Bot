import sys 
import numpy as np 
import MetaTrader5 as mt5 


def get_lot(balance):
    '''
    This function calculates the lot size for a given trade based on the current account balance.
    '''

    minimum, maximum = 1000, 2001
    while True:
        if int(balance) in np.arange(0, 501):
            return round((250/20000), 2)
        elif int(balance) in np.arange(500, 1001):
            return round((np.mean([500, 1000]) / 20000), 2)
        elif int(balance) in np.arange(minimum, maximum):
            return round((np.mean([minimum, maximum]) / 20000), 2)
        else:
            minimum += 1000
            maximum += 1000
            continue
    

def get_sl(entry, tp):
    '''
    This function calculates the stop loss value based on a risk-to-reward ratio (RRR) of 1.2\n
   
    Args:
        - entry: The trade entry price.
        - tp: take profit.
    '''

    return (entry - ((tp-entry)/1.2))


def Buy_req(symbol, entryp, min_val, avg_val):
    '''This function creates and returns a buy request.'''

    #Get lot amount 
    lot = get_lot(mt5.account_info()._asdict()['balance'])
    #Double the lot if price is closer to the average line
    if entryp >= np.mean([min_val, avg_val]): 
        lot = round(lot*2,2)

    #Get decimals for current symbol
    decimals = (5 if 'JPY' not in symbol else 3)
        
    #Create buy request
    req = {
        'action': mt5.TRADE_ACTION_DEAL,
        'symbol': symbol,
        'volume': lot,
        'type': mt5.ORDER_TYPE_BUY,
        'price': mt5.symbol_info_tick(symbol).ask,
        'sl': round(get_sl(entryp, avg_val), decimals),
        'tp': round(avg_val, decimals),
        'deviation': 1,
        'type_time': mt5.ORDER_TIME_GTC,
        'type_filling': mt5.ORDER_FILLING_FOK}
    
    return req 


def Sell_req(symbol, entryp, max_val, avg_val):
    '''This function creates and returns a sell request.'''

    #Get lot amount
    lot = get_lot(mt5.account_info()._asdict()['balance'])
    #Double the lot if price is closer to the average line
    if entryp <= np.mean([max_val, avg_val]):
        lot = round(lot*2,2)
    
    #Get decimals for current symbol
    decimals = (5 if 'JPY' not in symbol else 3)

    #Create sell request
    req = {
    'action': mt5.TRADE_ACTION_DEAL,
    'symbol': symbol,
    'volume': lot,
    'type': mt5.ORDER_TYPE_SELL,
    'price': mt5.symbol_info_tick(symbol).bid,
    'sl': round(get_sl(entryp, avg_val), decimals),
    'tp': round(avg_val, decimals),
    'deviation': 1,
    'type_time': mt5.ORDER_TIME_GTC,
    'type_filling': mt5.ORDER_FILLING_FOK }

    return req 


def Execute_Buy_Order(symbol, openp, min_val, avg_val):
    '''This function creates and sends a buy order.'''

    #Create buy request 
    buy_request = Buy_req(symbol, openp, min_val, avg_val)

    #Create buy order
    buy_order = mt5.order_send(buy_request)
    
    #Check Order Status
    if buy_order.retcode == mt5.TRADE_RETCODE_REQUOTE:
        print(f'\nRequote required! Trying again...')
        loop_n = 0
        while loop_n < 10:  #Try again 10 times...
            #Send order
            buy_request = Buy_req(symbol, openp, min_val, avg_val)
            buy_order = mt5.order_send(buy_request)
            if buy_order.retcode == mt5.TRADE_RETCODE_DONE:
                print(f"\nBuy order was executed successfully for {symbol},  position_id=#{buy_order.order}")
                break 
            else:
                loop_n += 1 
                continue
        
    elif buy_order.retcode == mt5.TRADE_RETCODE_DONE:
        print(f"\nBuy order was executed successfully for {symbol},  position_id=#{buy_order.order}")

    elif buy_order.retcode in (10015, 10016):
        print('Buy price or stop loss is invalid. Trying to send a buy order again...')
        loop_n = 0
        while loop_n < 15:     #try again 
            buy_request = Buy_req(symbol, openp, min_val, avg_val)
            buy_order = mt5.order_send(buy_request)
            if buy_order.retcode == mt5.TRADE_RETCODE_DONE:
                print(f"Buy order was executed successfully,  position_id=#{buy_order.order}")
                break 
            else:
                loop_n += 1 
                continue
        if buy_order.retcode in (10015, 10016):
            print(f'Buy order for symbol {symbol} was not processed successfully,  retcode={buy_order.retcode}')
            print('Processing the next symbol...')

    else:
        print(f"\nBuy order for {symbol} was executed but failed, retcode={buy_order.retcode}")
        print(f"Request Details:\n {buy_request}\n")
        print('Shutting down the program...')
        mt5.shutdown()
        sys.exit()


def Execute_Sell_Order(symbol, openp, max_val, avg_val):
    '''This function creates and sends a sell order.'''
    
    #Create sell request
    sell_request = Sell_req(symbol, openp, max_val, avg_val)

    #Create sell order
    sell_order = mt5.order_send(sell_request)

    #Check Order Status 
    if sell_order.retcode == mt5.TRADE_RETCODE_REQUOTE:
        print('\nRequote required! Trying again...')
        loop_n = 0
        while loop_n < 10:     #Try again 10 times...           
            #send order
            sell_request = Sell_req(symbol, openp, max_val, avg_val)
            sell_order = mt5.order_send(sell_request)
            #check order status 
            if sell_order.retcode == mt5.TRADE_RETCODE_DONE:
                print(f"Sell order was executed successfully for {symbol},  position_id=#{sell_order.order}")
                break 
            else:
                loop_n += 1
                continue
    
    elif sell_order.retcode == mt5.TRADE_RETCODE_DONE:
        print(f"\nSell order was executed successfully for {symbol},  position_id=#{sell_order.order}")

    elif sell_order.retcode in (10015, 10016):
        print('Sell price or stop loss is invalid. Trying to send a sell order again...')
        loop_n = 0
        while loop_n < 15:     
            sell_request = Sell_req(symbol, openp, max_val, avg_val)
            sell_order = mt5.order_send(sell_request)
            if sell_order.retcode == mt5.TRADE_RETCODE_DONE:
                print(f"Sell order was executed successfully,  position_id=#{sell_order.order}")
                break 
            else:
                loop_n += 1
                continue
        if sell_order.retcode in (10015, 10016):
                print(f'Sell order for symbol {symbol} was not processed successfully,  retcode={sell_order.retcode}')
                print('Processing the next symbol...')

    else:
        print(f"\nSell order for {symbol} was executed but failed, retcode={sell_order.retcode}")
        print(f"Request Details:\n {sell_request}\n")
        print('Shutting down the program...')
        mt5.shutdown()
        sys.exit()

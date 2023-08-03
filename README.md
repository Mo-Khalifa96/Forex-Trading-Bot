# Forex Trading Bot

## About The Program
**This program is a forex trading bot that works on the popular trading platform, MetaTrader 5. It was created 
using Python to connect to the MetaTrader5 terminal and run on a personal PC. It presents one of my first attempts 
at using Python for algorithmic trading and trading bot design and implementation. It is meant to showcase a sample of 
my work in algorithmic trading and trading bot development, but I wouldn't advise using it for personal trading.**
<br>
<br>
**This bot employs a variation of a SuperTrend strategy, translated from Pinescript to Python, using 18 periods and a 
multiplicative factor of 5, which analyzes market prices for a given forex pair and specifies the buy and sell conditions 
accordingly. To be more specific, the SuperTrend indicator identifies market trends, detecting the market's up-trend 
and down-trend which are depicted as a green or red line, according to which a decision can be made about buying or selling. 
These lines are not plotted by the bot here, however they are indicated by two key variables: maximum and minimum (and average, 
corresponding to the midway point). For the current strategy, the buy condition is defined as, buy if the low price of the next to 
last candle is lower than the indicator's down-trend line; whereas the sell condition is defined as, sell if the high price of 
the next to last candle is higher than the indicator's up-trend. The bot provides ongoing monitoring of market trends on each 
candle update for a given forex pair based on a prespecified timeframe and executes a buy/sell order if a buy/sell condition is met.**
<br>
<br>
**The program is split into 4 Python files, the main program script, 'Forex Trading Bot.py', and three additional scripts, each 
containing custom functions that are specialized for a particular type of task: 'DataProcessing.py', which contains the bot's 
indicator function for processing, analyzing, and identifying market trends; 'OrderProcessing.py', which is particularly 
specialized for processing market orders, covering custom functions for calculating the lot size for a given trade, stop 
loss and take profit values, and functions for executing buy and sell orders; and, 'TimeProcessing.py', which is specialized 
for time-related processes, such as monitoring market opening and closing times, monitoring and signalling the start of a new 
candle update for a given pair to begin analyzing its candles, and specifying the timeframes for trading.**
<br>
<br>
**This bot is designed to trade on multiple forex pairs simultaneously with different trading time frames, currently containing 26 pairs 
in total, each has its own trading timeframe. They are presented is a tuple of lists, each list containing the pair's name on MetaTrader,
the timeframe for trading on it, and a boolean value indicating the presence or absence of a new candle update for that given pair based on 
that particular timeframe. As such, each forex pair is processed and analyzed separately based on its own unique, prespecified trading 
timeframe. You can add or remove a pair from the tuple, or change the timeframe for any given pair. With a few tinkering, this bot can 
also trade on stocks and crypto, depending on the type of broker.**
<br>
<br>
**Finally, this bot is highly dynamic and responsive with multiple nested loops to control for: market open/close time, internet connection 
problems, order execution problems, high increases or decreases in the account balance, among others, and adjusts its behaviour accordingly. In 
this way it can confront and meet many different challenges automatically without intervention from the user.** 

<br>

**Overall, the bot performs the following tasks:**
 - **Checks if the forex market is open** <br>
 - **Connects to metatrader5 terminal and logs in to personal account** <br> 
 - **Checks if the internet is connected** <br>
 - **Iterates over forex pairs and collects candlesticks with open, high, low, and close prices for a given pair** <br>
 - **Applies the strategy or indicator to analyze the pair's candlesticks and identify its market trends** <br>
 - **Specifies the buy and sell conditions based on the indicator's analysis** <br>
 - **Executes a buy or sell order if the conditions are met** <br><br>
*It's also provided with a function that checks whether the data of a given pair was analyzed and prevents processing the same candlestick twice for a given timeframe*

<br>

## Executing the Program 
**To execute the trading bot, you can download the files and run the 'Forex Trading Bot.py' script or run the program 
from the Jupyter Notebook file provided. You can find more details on how to run the program on Jupyter inside the notebook
file. In either case, before executing the program, you will first have to download the MetaTrader5 terminal on your personal PC from [MetaTrader5](https://www.metatrader5.com/en/download), 
along with the relevant Python libraries, given that this bot must be connected to the MetaTrader5 terminal for it to work. Upon 
running the program, you will be prompted for three key inputs: your username, password, and your broker's server on MetaTrader5. 
Once it is put into action, you can track and inspect your market orders on the MetaTrader5 terminal itself. Feel free to try it on 
demo accounts with virtual money.**

<br>

**You can quickly access the code and execute the program from the link I have provided below. The link will direct you to a Jupyter Notebook, 
with the code and function files necessary to run the bot. I have provided more details on how to run the program on Jupyter inside the notebook.**
<br>

***To quickly access the main program and execute it on Jupyter, click on the link below:*** <br>
https://mybinder.org/v2/gh/Mo-Khalifa96/Forex-Trading-Bot/main?labpath=Forex%20Trading%20Bot%20(Jupyter%20version).ipynb

<br>

## Disclaimer 
It's important to note once more that strategy being employed here is not granteed to be successful. You're highly advised 
against using it for trading. A good strategy would require careful and exhaustive backtesting first before putting 
it into use. It is only meant to showcase what I've learned about algorithmic trading and my ability to utilize Python 
for developing and implementing trading bots. If you're intending on trying it, use it on a demo account for safety.
<br>
<br>

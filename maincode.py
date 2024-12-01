# 1) --- FETCHING LIVE STOCK PRICES ---

# the module yfinance is necessary to fetch live stock prices from yahoo finance API
import yfinance as yf 
import numpy as np
import pandas as pd

# define the stocks traded in the game
stocks={"Nvidia":"NVDA","Meta":"META","Microsoft":"MSFT","Alphabet":"GOOGL","AMD":"AMD"}
print(f"the stocks being traded are:{stocks.keys()}")

livestock_prices={}
stockprices_history=pd.DataFrame(columns=["name","price"]) #store all the stock prices (inclusive forecasts) in a dataframe as an history

def get_live_data():
    """ Fetch live stock prices from Yahoo finance API and store the prices in a dictionary""" 
    for names,symbol in stocks.items():
        try:
            stock=yf.Ticker(symbol) 

            #stock.history is a dataframe. The following line captures the item on the last row of the column "close"
            #iloc[0] selects the first item of the series obtained by stock.history(period="1d").tail(1)["close"]
            price=stock.history(period="1d").tail(1)["close"].iloc[0]
            #corresponding prices added to the prices dictionary
            livestock_prices[names]=price
        except Exception as e:
            print(f"Error while fetching data for {names}:{symbol}. Error type = {e}")

    #update the history with the live prices
    for names, prices in livestock_prices.items():
         price_history=stockprices_history.append({"name":names,"price":prices},ignore_index=True)

    return livestock_prices


print("Here are the current stock prices:",get_live_data())

#2) --- SIMULATION OF STOCK PRICES FOR THE GAME ---


list_lastprices=livestock_prices #for the 1st period, last prices = live prices. This variable is updated each period with the function "simulate_stock_prices"

def simulate_stock_prices():
    """This function forecasts stock prices for the next period based on the live stock data fetched with the function get_live_data. The forecast is
    an AR(1) model (random walk). Random walk model: P_t+1 = alpha + beta*P_t + error term"""
    simulated_prices={} #local variable
    for names,last_price in list_lastprices.items():
        alpha=0 #drift set to 0
        beta=1 #condition for random walk models
        errorterm=np.random.normal(0,1) #white noise normally distributed with mean==0 and standard deviation==1
        price_forecast=alpha+beta*last_price+errorterm
        simulated_prices[names]=price_forecast

    #update the last prices dictionary for when the function is called next period
    list_lastprices=simulated_prices

    #update the stock prices history
    for names, prices in list_lastprices.items():
         stockprices_history.loc[len(stockprices_history)]={"name":names,"price":prices} #add a new row to the dataframe
    return simulated_prices   






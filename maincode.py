#! C:\Users\dorin\OneDrive\Documents\Université\HSG\SA2024\XCampHSG\Group project\PythonprojectHSG\venvtradinggame\Scripts\python.exe

# 1) --- FETCHING LIVE STOCK PRICES ---

# the module yfinance is necessary to fetch live stock prices from yahoo finance API
import yfinance as yf 
import numpy as np
import pandas as pd


# define the stocks traded in the game
stocks={"Nvidia":"NVDA","Meta":"META","Microsoft":"MSFT","Alphabet":"GOOGL","AMD":"AMD"}
print(f"the stocks being traded are:{list(stocks.keys())}") #converted into a list for a better output

livestock_prices={}
stockprices_history=pd.DataFrame(columns=["name","price"]) #store all the stock prices (inclusive forecasts) in a dataframe as an history


def get_live_data():
    """ Fetch live stock prices from Yahoo finance API and store the prices in a dictionary""" 
    #global variables modified whithin the function
    global livestock_prices
    global stockprices_history

    for names,symbol in stocks.items():
        try:
            stock=yf.Ticker(symbol) 
            #stock.history is a dataframe. The following line captures the item on the last row of the column "close"
            #iloc[0] selects the first item of the series obtained by stock.history(period="1d").tail(1)["close"]
            price=stock.history(period="1d").tail(1)["Close"].iloc[0]
            #corresponding prices added to the prices dictionary
            livestock_prices[names]=price
        except Exception as e:
            print(f"Error while fetching data for {names}:{symbol}. Error type = {e}")

    #update the history with the live prices
    for names, prices in livestock_prices.items():
        stockprices_history.loc[len(stockprices_history)]={"name":names,"price":prices} #add a new row to the dataframe
       

    return livestock_prices


#print("Here are the current stock prices:",get_live_data())

#2) --- SIMULATION OF STOCK PRICES FOR THE GAME ---


list_lastprices=livestock_prices #for the 1st period, last prices = live prices. This variable is updated each period with the function "simulate_stock_prices"

def simulate_stock_prices():
    """This function forecasts stock prices for the next period based on the live stock data fetched with the function get_live_data. The forecast is
    an AR(1) model (random walk). Random walk model: P_t+1 = alpha + beta*P_t + error term"""
    simulated_prices={} #local variable
    global list_lastprices
    for names,last_price in list_lastprices.items():
        alpha=0 #drift set to 0
        beta=1 #condition for random walk models
        errorterm=np.random.normal(0,5) #white noise normally distributed with mean==0 and standard deviation==5
        price_forecast=alpha+beta*last_price+errorterm
        simulated_prices[names]=price_forecast

    #update the last prices dictionary for when the function is called next period
    list_lastprices=simulated_prices

    #update the stock prices history
    for names, prices in list_lastprices.items():
         stockprices_history.loc[len(stockprices_history)]={"name":names,"price":prices} 
    return simulated_prices   


def prepare_data(prices_list):
    """This function transforms the live stock prices and forecasted prices in an more readible way
    1st Step: the functions get_live_data() or simulate_stock_prices() should be called first
    
    Arguments: either 'list_lastprices' or 'livestock_prices'
    
    Return: stocks and prices rounded to two decimals """
    cleandata={}

    for stock, price in prices_list.items():
        cleandata[stock]=round(float(price),2)

    return cleandata



# --- FOR lEO AND TIM: FUNCTIONS TO RUN TO START THE GAME ---

#first round
get_live_data()
#next rounds
simulate_stock_prices()

#to display the stock prices (either list_lastprices as argument or livestock_prices if it is the first round)
#returns a dictionary
prices_game=prepare_data(list_lastprices)
print(prices_game)
print("history:",stockprices_history)

#### VISUALISATION PART:

import matplotlib.pyplot as plt

# Display Stock Prices
def display_stock_prices(prices, period):
    """
    Display stock prices in a readable format.
    
    Args:
        prices (dict): Dictionary of stock prices.
        period (int): Current period.
    """
    print(f"\n--- Stock Prices for Period {period} ---")
    for stock, price in prices.items():
        print(f"{stock}: ${price:.2f}")


# Track and Display Portfolio Performance
def calculate_portfolio_value(prices, allocations):
    """
    Calculate the portfolio value based on current stock prices and allocations.
    
    Args:
        prices (dict): Dictionary of stock prices.
        allocations (dict): Dictionary of allocations as percentages (0-100%).
    
    Returns:
        float: Total portfolio value.
    """
    total_value = 0
    for stock, allocation in allocations.items():
        total_value += prices.get(stock, 0) * (allocation / 100)
    return total_value


def display_results(user_value, ai_values):
    """
    Display the final results of the game.
    
    Args:
        user_value (float): Final portfolio value of the user.
        ai_values (list): Final portfolio values of all AI participants.
    """
    print("\n--- Final Results ---")
    
    # Include the user in rankings
    all_values = ai_values + [user_value]
    rankings = sorted(all_values, reverse=True)
    user_rank = rankings.index(user_value) + 1

    print(f"Your Final Portfolio Value: ${user_value:.2f}")
    print(f"Your Ranking: {user_rank}/{len(all_values)}")
    
    # Best and worst AI portfolio values
    best_ai = max(ai_values)
    worst_ai = min(ai_values)
    print(f"Best AI Portfolio Value: ${best_ai:.2f}")
    print(f"Worst AI Portfolio Value: ${worst_ai:.2f}")
    
    # Display all AI portfolio values
    print("\nAI Portfolio Values:")
    for i, value in enumerate(ai_values, start=1):
        print(f"AI {i}: ${value:.2f}")


# Visualization
def visualize_performance(history, user_values, ai_values, period_range):
    """
    Visualize stock price evolution and portfolio performance.
    
    Args:
        history (pd.DataFrame): Stock price history DataFrame.
        user_values (list): List of user's portfolio values over time.
        ai_values (list of lists): List of each AI's portfolio values over time.
        period_range (list): List of periods.
    """
    # Stock price evolution
    plt.figure(figsize=(10, 6))
    for stock in history['name'].unique():
        stock_data = history[history['name'] == stock]
        plt.plot(stock_data.index, stock_data['price'], label=stock)
    plt.title('Stock Price Evolution')
    plt.xlabel('Periods')
    plt.ylabel('Price')
    plt.legend()
    plt.show()

    # Portfolio performance
    plt.figure(figsize=(10, 6))
    plt.plot(period_range, user_values, label='User', linewidth=2)
    for i, ai_value in enumerate(ai_values):
        plt.plot(period_range, ai_value, label=f'AI {i + 1}', linestyle='--')
    plt.title('Portfolio Performance')
    plt.xlabel('Periods')
    plt.ylabel('Portfolio Value')
    plt.legend()
    plt.show()

#! C:\Users\dorin\OneDrive\Documents\Université\HSG\SA2024\XCampHSG\Group project\PythonprojectHSG\venvtradinggame\Scripts\python.exe

import yfinance as yf # the module yfinance is necessary to fetch live stock prices from yahoo finance API
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random


#0) GLOBAL VARIABLES DEFINITION

stocks={"Nvidia":"NVDA","Meta":"META","Microsoft":"MSFT","Alphabet":"GOOGL","AMD":"AMD"}# define the stocks traded in the game
livestock_prices={}
stockprices_history=pd.DataFrame(columns=["name","price"]) #store all the stock prices (inclusive forecasts) in a dataframe as an history
list_lastprices=livestock_prices #for the 1st period, last prices = live prices. This variable is updated each period with the function "simulate_stock_prices"
period=0

#1) FUNCTIONS DEFINITION


def get_live_data():
    """Fetch live stock prices from Yahoo finance API and store the prices in a dictionary
    
    return: live stock prices from the last trading day""" 
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
        #in case fetching the data from yfinance doesn't work, random prices are used to continue the game
        except Exception as e:
            print(f"Error while fetching data for {names}:{symbol}. Error type = {e}")
            print("Using mock data instead.")
            livestock_prices[names] = np.random.uniform(100, 500)

    #update the history with the live prices
    for names, prices in livestock_prices.items():
        stockprices_history.loc[len(stockprices_history)]={"name":names,"price":prices} #add a new row to the dataframe
       

    return livestock_prices


def simulate_stock_prices():
    """This function forecasts stock prices for the next period based on the live stock data fetched with the function get_live_data. The forecast is
    an AR(1) model (random walk). Random walk model: P_t+1 = alpha + beta*P_t + error term"""
    simulated_prices={} #local variable
    global list_lastprices
    global period
    period += 1
    for names,last_price in list_lastprices.items():
        alpha=0 #drift set to 0
        beta=1 #condition for random walk models
        errorterm=np.random.normal(0,5) #white noise normally distributed with mean==0 and standard deviation==5 (higher stdev to allow for higher volatility in the game)
        price_forecast=alpha+beta*last_price+errorterm
        simulated_prices[names]=price_forecast

    #update the last prices dictionary for when the function is called next period
    list_lastprices=simulated_prices

    #update the stock prices history
    for names, prices in list_lastprices.items():
         stockprices_history.loc[len(stockprices_history)]={"name":names,"price":prices} 
    return simulated_prices   

def simulate_stock_prices_shock():
    """This function forecasts stock prices for the next period based on the live stock data fetched with the function get_live_data. a
     stock price crash is simulated. """
    simulated_prices={} #local variable
    global list_lastprices
    global period
    period += 1
    for names,last_price in list_lastprices.items():
        alpha=0 #drift set to 0
        beta=-10 #negative beta coefficient to push the prices
        errorterm=np.random.normal(0,5) #white noise normally distributed with mean==0 and standard deviation==5
        price_forecast=alpha+beta*last_price+errorterm
        simulated_prices[names]=price_forecast

    #update the last prices dictionary for when the function is called next period
    list_lastprices=simulated_prices

    #update the stock prices history
    for names, prices in list_lastprices.items():
         stockprices_history.loc[len(stockprices_history)]={"name":names,"price":prices} 
    return simulated_prices   


def simulate_stock_prices_goodstate():
    """This function forecasts stock prices for the next period based on the live stock data fetched with the function get_live_data. 
    An unexpected increase in the stock prices is simulated"""
    simulated_prices={} #local variable
    global list_lastprices
    global period
    period += 1
    for names,last_price in list_lastprices.items():
        alpha=0 #drift set to 0
        beta=5 #higher positive beta to force the prices up
        errorterm=np.random.normal(0,5) #white noise normally distributed with mean==0 and standard deviation==5
        price_forecast=alpha+beta*last_price+errorterm
        simulated_prices[names]=price_forecast

    #update the last prices dictionary for when the function is called next period
    list_lastprices=simulated_prices

    #update the stock prices history
    for names, prices in list_lastprices.items():
         stockprices_history.loc[len(stockprices_history)]={"name":names,"price":prices} 
    return simulated_prices   


def launch_prices_forecast():
    """This function randomly determines which function will be used to forecast the next stock prices (random walk, shock or goodstate)
    return: simulated_prices through the function being called"""

    forecast=random.choice([simulate_stock_prices,simulate_stock_prices_goodstate,simulate_stock_prices_shock]) #one of the 3 functions is chosen
    simulated_prices=forecast() #chosen function is called and forecast of prices is made
    
    #message to the player
    if forecast==simulate_stock_prices:
        print("no specific news about the stock markets")
    elif forecast==simulate_stock_prices_goodstate:
        print("News: overall good state of the economy and positive prospects regarding the market returns")
    elif forecast==simulate_stock_prices_shock:
        print("News: unexpected shock will disturb the actual trends. Investors should be cautious.")

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


#after using the get live data function, and the prepare data function
def start_allocation(stock_data):
    """This function defines the portfolio allocations of the user.
    
    Arguments:
        stock_data (dict): Dictionary with stock names and prices.
    
    Returns:
        list: A list with the allocations to each stock (exposure short/long).
    """
    print("Allocate your portfolio. You can use leverage up to 5x or short stocks.")
    print(f"Available stocks: {list(stock_data.keys())}")
    print("Instructions:\nYou can allocate a total of up to 500% across all stocks, using leverage up to 5x. "
          "Negative values represent short selling.\nThe sum of all allocations must be up to 500% (you can use leverage up to 5x).")

    user_allocation = []
    total_allocation = 0  # Track cumulative allocation
    
    # Loop through all stocks to collect allocations
    for stock in stock_data.keys():
        while True:  # Ensure valid input for each stock
            try:
                allocation = float(input(f"Enter % allocation to {stock} (can be negative for short positions): "))
                if total_allocation + abs(allocation) > 500:  # Check leverage constraint
                    print("Total allocation exceeds allowed leverage (500%). Please enter a smaller value.")
                else:
                    user_allocation.append(allocation)
                    total_allocation += abs(allocation)  # Update total absolute allocation
                    break
            except ValueError:
                print("Invalid input. Please enter numeric values only.")

    print("\nYour portfolio allocation:")
    for stock, allocation in zip(stock_data.keys(), user_allocation):
        print(f"{stock}: {allocation}%")
    return user_allocation


def calculate_returns(allocation, stock_data, start_prices, end_prices):
    start_prices = np.array([start_prices[stock] for stock in stock_data.keys()])
    end_prices = np.array([end_prices[stock] for stock in stock_data.keys()])

    return np.sum(np.array(allocation) * (end_prices / start_prices - 1))

#after using the simulate price function
def display_stock_prices(prices):
    """ This function displays the stock prices for a specific period
    Arguments: a dictionary with stocks and their prices, the current period as integer"""
    global period
    print(f"--- Stock Prices for Period {period} ---")
    for stock, price in prices.items():
        print(f"{stock}: ${price:.2f}")
    
    

#at the end, to close the game
def display_results(user_value, ai_values):
    """ This function displays the results obtained by the human user and the bots he is playing against
    Arguments: user overall performance, list of bots performances """

    print("--- Final Results ---")
    all_values = ai_values + [user_value]
    rankings = sorted(all_values, reverse=True)
    user_rank = rankings.index(user_value) + 1

    print(f"Your Final Portfolio Value: ${user_value:.2f}")
    print(f"Your Ranking: {user_rank}/{len(all_values)}")
    best_ai = max(ai_values)
    worst_ai = min(ai_values)
    print(f"Best AI Portfolio Value: ${best_ai:.2f}")
    print(f"Worst AI Portfolio Value: ${worst_ai:.2f}")
    print("AI Portfolio Values:")
    for i, value in enumerate(ai_values, start=1):
        print(f"AI {i}: ${value:.2f}")
    
    #the game ends, the user is asked to whether to start again or quit
    play_again = input("Would you like to play again? If so, type 'yes'")
    if play_again.lower() == "yes":
        trading_game()
    else:
        print("Thank you for playing!")

# last function to call

def visualize_performance(history, user_values, ai_values, period_range):
    """ Visualize stock returns evolution and portfolio performance.
    Arguments:
    history (pd.DataFrame): Stock price history DataFrame.
    user_values (list): List of user's portfolio values over time.
    ai_values (list of lists): List of each AI's portfolio values over time.
    period_range (list): List of periods. """

    # Calculate returns for stock prices
    history['return'] = history.groupby('name')['price'].pct_change() * 100

    # Plot stock returns evolution
    plt.figure(figsize=(10, 6))
    for stock in history['name'].unique():
        stock_data = history[history['name'] == stock]
        plt.plot(stock_data.index, stock_data['return'], label=stock)
    plt.title('Stock Returns Evolution')
    plt.xlabel('Periods')
    plt.ylabel('Returns (%)')
    plt.axhline(0, color='gray', linestyle='--', linewidth=0.8)  # Add a baseline for 0% return
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





# --- Main Game ---


def trading_game():
    """ When called, this function launches the game. The game is integrated into a function to allow for playing many times."""

    gamerunning= "" 
    print("Welcome to the Trading Game!")
    print("""
    Rules:
    1. Allocate your portfolio among 5 stocks with leverage up to 5x.
    2. You can use leverage to allocate up to 500% across all stocks, or short stocks by using negative allocations.
    3. Stock prices are fetched live for the first round. Subsequent rounds simulate prices.
    4. Your goal is to maximize returns compared to 9 AI players.""")
        
    while gamerunning != "go":
        gamerunning=input("write 'go' when you're ready to start!")
       
        
    global stocks
    print(f"The stocks being traded are: {list(stocks.keys())}") #converted into a list for a more readible output

    # User inputs the number of periods for the game
    num_periods=0
    while num_periods<=0:
        try:
            num_periods = int(input("Enter the number of rounds (at least 2) you'd like the game to run (e.g., 5, 10): "))
            if num_periods <= 1:
                print("Please enter a positive number greater than 1.")
            else:
                break
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    live_prices = get_live_data()  # Fetch stock prices for the first round
    display_stock_prices(live_prices)  # Display live prices to the user
    user_allocation = start_allocation(live_prices)  # User inputs portfolio allocation percentages

    # Variables' initialisation
    user_portfolio_value = 100  # user
    ai_portfolio_values = [100] * 9  # nine AI players

    # AI random portfolio allocations
    ai_allocations = [
        np.random.dirichlet(np.ones(len(live_prices))) * 100 for _ in range(9)
    ]  # generate random AI portfolio allocations summing to 100%

    # initialize lists for tracking portfolio values over time
    user_values = [user_portfolio_value]
    ai_values = [[value] for value in ai_portfolio_values]
    period_range = [0]  # initialize periods for visualization

    previous_prices = live_prices  # set starting prices for the first period

    # Game Loop (for each of the periods)
    for period in range(1, num_periods + 1):  # loop through all periods
        print(f"\n--- Period {period} ---")
        period_range.append(period)  # add current period to the list for tracking

        # Forecast stock prices for the current period
        stock_data = launch_prices_forecast()  # randomly simulate stock prices for this round
        stock_data_cleaned = prepare_data(stock_data)  # clean and format simulated prices
        display_stock_prices(stock_data_cleaned)  # display stock prices to the user

        # User's portfolio update
        user_return = calculate_returns(
            user_allocation, stock_data_cleaned, previous_prices, stock_data_cleaned
        )  # calculate user return
        user_portfolio_value *= (1 + user_return)
        user_values.append(user_portfolio_value)  # append the updated value to the list

        # AI's portfolio update
        for i, ai_allocation in enumerate(ai_allocations):
            ai_return = calculate_returns(
                ai_allocation, stock_data_cleaned, previous_prices, stock_data_cleaned
            )  # Calculate AI return
            ai_portfolio_values[i] *= (1 + ai_return)  # update AI portfolio value
            ai_values[i].append(ai_portfolio_values[i])  # append updated value

        # Update previous prices for the next period
        previous_prices = stock_data_cleaned

        # Diplay portfolio
        print(f"\nYour Portfolio Value: ${user_portfolio_value:.2f}")  # show user portfolio value
        for i, ai_value in enumerate(ai_portfolio_values):
            print(f"AI {i + 1} Portfolio Value: ${ai_value:.2f}")  # show AI portfolio values

        # pause to allow the user to review before continuing
        input("Press Enter to continue to the next period...")

    # Display of the results
    display_results(user_values[-1], [ai_values[i][-1] for i in range(9)])  # show results for user and AI players
    visualize_performance(stockprices_history, user_values, ai_values, period_range)  # generate performance graphs
    
if __name__ == "__main__":
    trading_game()

print(stockprices_history)
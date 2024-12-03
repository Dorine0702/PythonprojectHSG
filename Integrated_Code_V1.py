import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Global variables
livestock_prices = {}
stockprices_history = pd.DataFrame(columns=["name", "price"])
list_lastprices = {}

# --- Fetch Live Stock Prices ---
def get_live_data():
    """
    Fetch live stock prices from Yahoo Finance API.
    Use mock data if API calls fail.
    """
    global livestock_prices, stockprices_history

    print("\nFetching live stock prices...")
    for name, symbol in stocks.items():
        try:
            stock = yf.Ticker(symbol)
            price = stock.history(period="1d").tail(1)["Close"].iloc[0]
            livestock_prices[name] = price
        except Exception as e:
            print(f"Error while fetching data for {name} ({symbol}): {e}")
            print("Using mock data instead.")
            livestock_prices[name] = np.random.uniform(100, 500)

    for name, price in livestock_prices.items():
        stockprices_history.loc[len(stockprices_history)] = {"name": name, "price": price}

    print("Stock prices ready!")
    return livestock_prices

# --- Simulate Stock Prices ---
def simulate_stock_prices():
    global list_lastprices, stockprices_history

    if not list_lastprices:
        list_lastprices = livestock_prices.copy()

    simulated_prices = {}
    for name, last_price in list_lastprices.items():
        alpha = 0
        beta = 1
        errorterm = np.random.normal(0, 5)
        price_forecast = alpha + beta * last_price + errorterm
        simulated_prices[name] = max(price_forecast, 0)

    list_lastprices = simulated_prices
    for name, price in list_lastprices.items():
        stockprices_history.loc[len(stockprices_history)] = {"name": name, "price": price}

    return simulated_prices

# --- Prepare Data for Display ---
def prepare_data(prices_list):
    return {stock: round(float(price), 2) for stock, price in prices_list.items()}

# --- Portfolio Allocation ---
def start_game(stock_data, leverage=5):
    print("\nAllocate your portfolio. You can use leverage up to 5x or short stocks.")
    print(f"Available stocks: {list(stock_data.keys())}")
    print("""Instructions:
    - You can allocate a total of up to 500% across all stocks, using leverage up to 5x. Negative values represent short selling.
    - The sum of all allocations must be up to 500% (you can use leverage up to 5x).
    """)

    user_allocation = []
    while True:
        try:
            for stock in stock_data.keys():
                allocation = float(input(f"Enter % allocation to {stock} (can be negative for short positions): "))
                user_allocation.append(allocation)

            total_absolute_allocation = sum(abs(a) for a in user_allocation)

            if total_absolute_allocation > 500:
                print(f"Total allocation exceeds allowed leverage (500%). Please try again.")
                user_allocation = []
            else:
                break
        except ValueError as e:
            print(f"Invalid input: {e}. Please enter numeric values only.")
            user_allocation = []

    print("\nYour portfolio allocation:")
    for stock, allocation in zip(stock_data.keys(), user_allocation):
        print(f"{stock}: {allocation}%")
    return user_allocation

# --- Calculate Returns ---
def calculate_returns(allocation, stock_data, start_prices, end_prices):
    start_prices = np.array([start_prices[stock] for stock in stock_data.keys()])
    end_prices = np.array([end_prices[stock] for stock in stock_data.keys()])
    return np.sum(np.array(allocation) * (end_prices / start_prices - 1))

# --- Display Stock Prices ---
def display_stock_prices(prices, period):
    print(f"\n--- Stock Prices for Period {period} ---")
    for stock, price in prices.items():
        print(f"{stock}: ${price:.2f}")

# --- Display Results ---
def display_results(user_value, ai_values):
    print("\n--- Final Results ---")
    all_values = ai_values + [user_value]
    rankings = sorted(all_values, reverse=True)
    user_rank = rankings.index(user_value) + 1

    print(f"Your Final Portfolio Value: ${user_value:.2f}")
    print(f"Your Ranking: {user_rank}/{len(all_values)}")
    best_ai = max(ai_values)
    worst_ai = min(ai_values)
    print(f"Best AI Portfolio Value: ${best_ai:.2f}")
    print(f"Worst AI Portfolio Value: ${worst_ai:.2f}")
    print("\nAI Portfolio Values:")
    for i, value in enumerate(ai_values, start=1):
        print(f"AI {i}: ${value:.2f}")
    print("Would you like to play again? If so, type 'yes'")
    play_again = input()
    if play_again.lower() == "yes":
        trading_game()
    else:
        print("Thank you for playing!")


# --- Visualize Performance ---
def visualize_performance(history, user_values, ai_values, period_range):
    plt.figure(figsize=(10, 6))
    for stock in history['name'].unique():
        stock_data = history[history['name'] == stock]
        plt.plot(stock_data.index, stock_data['price'], label=stock)
    plt.title('Stock Price Evolution')
    plt.xlabel('Periods')
    plt.ylabel('Price')
    plt.legend()
    plt.show()

    plt.figure(figsize=(10, 6))
    plt.plot(period_range, user_values, label='User', linewidth=2)
    for i, ai_value in enumerate(ai_values):
        plt.plot(period_range, ai_value, label=f'AI {i + 1}', linestyle='--')
    plt.title('Portfolio Performance')
    plt.xlabel('Periods')
    plt.ylabel('Portfolio Value')
    plt.legend()
    plt.show()

# --- Main Game Loop ---
def trading_game():
    while True:
        print("\nWelcome to the Trading Game!")
        print("""
        Rules:
        1. Allocate your portfolio among 5 stocks with leverage up to 5x.
        2. You can use leverage to allocate up to 500% across all stocks, or short stocks by using negative allocations.
        3. Stock prices are fetched live for the first round. Subsequent rounds simulate prices.
        4. Your goal is to maximize returns compared to 9 AI players.

        Press Enter when you're ready to start!
        """)
        input()

        global stocks
        stocks = {"Nvidia": "NVDA", "Meta": "META", "Microsoft": "MSFT", "Alphabet": "GOOGL", "AMD": "AMD"}
        print(f"The stocks being traded are: {list(stocks.keys())}")

        # User inputs the number of periods for the game
        while True:
            try:
                num_periods = int(input("\nEnter the number of periods (at least 2) you'd like the game to run (e.g., 5, 10): "))
                if num_periods <= 1:
                    print("Please enter a positive number greater than 1.")
                else:
                    break
            except ValueError:
                print("Invalid input. Please enter a valid number.")

        live_prices = get_live_data()

        # Show stock prices before allocation
        display_stock_prices(live_prices, period=0)

        user_allocation = start_game(live_prices)

        user_return = 0
        ai_allocations = [
            np.random.dirichlet(np.ones(len(live_prices))) * 100 for _ in range(9)
        ]
        ai_returns = [0] * 9
        user_values = []
        ai_values = [[] for _ in range(9)]
        period_range = []

        for period in range(1, num_periods + 1):
            print(f"\n--- Period {period} ---")
            period_range.append(period)

            if period == 1:
                stock_data = live_prices
            else:
                stock_data = simulate_stock_prices()

            stock_data_cleaned = prepare_data(stock_data)
            display_stock_prices(stock_data_cleaned, period)

            if period > 1:
                user_return += calculate_returns(
                    user_allocation, stock_data_cleaned, previous_prices, stock_data_cleaned
                )

            user_values.append(user_return)
            for i, ai_allocation in enumerate(ai_allocations):
                if period > 1:
                    ai_returns[i] += calculate_returns(
                        ai_allocation, stock_data_cleaned, previous_prices, stock_data_cleaned
                    )
                ai_values[i].append(ai_returns[i])

            previous_prices = stock_data_cleaned
            input("\nPress Enter to continue to the next period...")

        display_results(user_values[-1], ai_returns)
        visualize_performance(stockprices_history, user_values, ai_values, period_range)

if __name__ == "__main__":
    trading_game()

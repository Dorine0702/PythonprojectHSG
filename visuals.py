import matplotlib.pyplot as plt

# --- Display Stock Prices ---
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


# --- Track and Display Portfolio Performance ---
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


# --- Visualization (Optional) ---
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
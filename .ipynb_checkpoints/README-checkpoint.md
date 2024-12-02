# PythonprojectHSG
Trading Game
Part1: Data Handling and Stock Price Simulation

Responsibilities:
	1.	Live Stock Price Data Integration:
	•	Write functions to fetch live stock price data using APIs like yfinance or Alpha Vantage.
	•	Ensure the data pipeline is robust, handling errors (e.g., API limits, network issues).
	•	Provide an interface to allow switching between live data and simulated data for testing.
	2.	Random Walk Stock Price Simulation:
	•	Implement AR(1) simulation for stock price movements.
	•	Write modular functions to generate and return simulated stock prices based on parameters like periods and initial price.
	3.	Data Management:
	•	Prepare stock data (live or simulated) for game use by ensuring consistent formats.
	•	Provide helper functions to fetch stock prices at any time step.

Deliverables:
	•	Functions: get_live_data(), simulate_stock_prices(), prepare_data().

Part2: Game Logic and AI Implementation

Responsibilities:
	1.	Game Setup and Flow:
	•	Write the main game loop:
	•	Prompt the user to start the game, set trade frequency, and define the number of periods.
	•	Call relevant functions to fetch/display stock data.
	•	Implement bankruptcy checks (e.g., halt the game if the user’s portfolio value hits zero or goes negative).
	2.	Portfolio Allocation System:
	•	Allow user to input portfolio allocation, ensuring inputs are validated (e.g., sum equals 100%, leverage constraints).
	•	Calculate portfolio returns based on stock price changes.
	•	Enforce rules like no changes in portfolio allocation after the first round (if applicable).
	3.	AI Competitors:
	•	Write logic for generating random portfolio allocations for 9 AI players.
	•	Track and compute returns for each AI participant.

Deliverables:
	•	Functions: start_game(), calculate_returns(), generate_ai_allocations().

Part3: User Interaction and Results Display

Responsibilities:
	1.	User Interaction:
	•	Create user prompts for inputs (using input() in IDLE or cell-based prompts in Jupyter).
	•	Display current stock prices and portfolio performance clearly in text format.
	•	Provide feedback for invalid inputs (e.g., exceeding leverage).
	2.	Results Tracking and Display:
	•	Write functions to calculate and display user and AI portfolio values at each step.
	•	Summarize results at the end, including:
	•	User’s final portfolio value and ranking against AI.
	•	Performance of the best and worst AI portfolios (and optionally all AI).
	•	Display price evolution of stocks in a clean textual summary (tables or inline charts in Jupyter).
	3.	Visualization (Optional for Jupyter):
	•	If using Jupyter, leverage libraries like Matplotlib or Plotly for visualizing price changes or portfolio performance.

Deliverables:
	•	Functions: display_stock_prices(), display_results(), visualize_performance().

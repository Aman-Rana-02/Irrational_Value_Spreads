#### Preamble ####
# Purpose: Simulates a dataset of efficient and inefficient market returns
# Author: Aman Rana
# Date: 22 November 2024
# Contact: aman.rana@mail.utoronto.ca
# License: MIT
# Pre-requisites: 
#  - `pandas` must be installed (pip install pandas)
#  - `numpy` must be installed (pip install numpy)
#  - `pyarrow` must be installed (pip install pyarrow)
#  - `matplotlib` must be installed (pip install matplotlib)
#  - `utils/utils.py` must be available
#  - `warnings` must be available (part of Python's standard library)

#### Workspace setup ####
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
from utils.utils import get_return_windows
warnings.simplefilter(action='ignore', category=pd.errors.SettingWithCopyWarning)

np.random.seed(304)

#### Simulate data ####
# We will simulate three instances of a timeseries of returns from 1927 to 2024
# The first timeseries will be returns in an efficient market, where prices are a random walk
# The second timeseries will be returns in an inefficient market, where returns are an AR(1) process
# The third timeseries will be returns in an evolutionary market,
# which slips in and out of efficient and inefficient regimes

date_df = pd.DataFrame()
date_df['Date'] = pd.date_range(start='1/1/1927', end='22/11/2024', freq='M')
efficient_df = date_df.copy()
inefficient_df = date_df.copy()
evolutionary_df = date_df.copy()

# Simulate efficient market prices
# Efficient market returns are random, making price a random walk
number_of_efficient_price_paths = 100
multiple_efficient_df = pd.DataFrame()
for i in range(number_of_efficient_price_paths):
    print("Processing efficient market path: ", i, end='\r')
    efficient_returns = np.random.normal(0, 0.01, len(efficient_df))
    efficient_prices = 100 * np.exp(np.cumsum(efficient_returns))
    temp_df = date_df.copy()
    temp_df['Adj Close'] = efficient_prices
    temp_df['Log Return'] = np.log(temp_df['Adj Close']).diff()
    temp_df['Price Path'] = i
    temp_df = get_return_windows(temp_df)
    multiple_efficient_df = pd.concat([multiple_efficient_df, temp_df])

efficient_returns = np.random.normal(0, 0.01, len(efficient_df))
efficient_prices = 100 * np.exp(np.cumsum(efficient_returns))
efficient_df['Adj Close'] = efficient_prices

# Simulate inefficient market prices
# Inefficient market returns are an AR(1) process
phi = 0.5

number_of_inefficient_price_paths = 100
multiple_inefficient_df = pd.DataFrame()
for i in range(number_of_efficient_price_paths):
    print("Processing inefficient market path: ", i, end='\r')
    noise = np.random.normal(0, 0.01, len(inefficient_df))
    inefficient_returns = np.zeros(len(inefficient_df))
    for t in range(1, len(inefficient_df)):
        inefficient_returns[t] = phi * inefficient_returns[t - 1] + noise[t]
    inefficient_prices = 100 * np.exp(np.cumsum(inefficient_returns))
    temp_df = date_df.copy()
    temp_df['Adj Close'] = inefficient_prices
    temp_df['Log Return'] = np.log(temp_df['Adj Close']).diff()
    temp_df['Price Path'] = i
    temp_df = get_return_windows(temp_df)
    multiple_inefficient_df = pd.concat([multiple_inefficient_df, temp_df])

noise = np.random.normal(0, 0.01, len(inefficient_df))
inefficient_returns = np.zeros(len(inefficient_df))

for t in range(1, len(inefficient_df)):
    inefficient_returns[t] = phi * inefficient_returns[t - 1] + noise[t]

inefficient_prices = 100 * np.exp(np.cumsum(inefficient_returns))
inefficient_df['Adj Close'] = inefficient_prices

# Log return
efficient_df['Log Return'] = np.log(efficient_df['Adj Close']).diff()
inefficient_df['Log Return'] = np.log(inefficient_df['Adj Close']).diff()

efficient_df.to_parquet('../data/00-simulated_data/efficient_market_prices.parquet')
inefficient_df.to_parquet('../data/00-simulated_data/inefficient_market_prices.parquet')
multiple_efficient_df.to_parquet('../data/00-simulated_data/multiple_efficient_market_prices.parquet')
multiple_inefficient_df.to_parquet('../data/00-simulated_data/multiple_inefficient_market_prices.parquet')

# Plot the simulated data
plt.figure(figsize=(12, 6))
plt.plot(efficient_df['Date'], efficient_df['Adj Close'], label='Efficient Market')
plt.plot(inefficient_df['Date'], inefficient_df['Adj Close'], label='Inefficient Market')
plt.xlabel('Date')
plt.ylabel('Price')
plt.title('Simulated Market Prices')
plt.legend()
plt.savefig('../figs/Sample_Simulated_Market_Prices.png')

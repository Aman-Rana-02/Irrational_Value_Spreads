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

#### Workspace setup ####
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(304)

#### Simulate data ####
# We will simulate three instances of a timeseries of returns from 1927 to 2024
# The first timeseries will be returns in an efficient market, where prices are a random walk
# The second timeseries will be returns in an inefficient market, where returns are an AR(1) process
# The third timeseries will be returns in an evolutionary market,
# which slips in and out of efficient and inefficient regimes

efficient_df = pd.DataFrame()
efficient_df['date'] = pd.date_range(start='1/1/1927', end='22/11/2024', freq='M')
inefficient_df = efficient_df.copy()
evolutionary_df = efficient_df.copy()

# Simulate efficient market prices
# Efficient market returns are random, making price a random walk
efficient_returns = np.random.normal(0, 0.01, len(efficient_df))
efficient_prices = 100 * (1 + efficient_returns).cumprod()
efficient_df['price'] = efficient_prices

# Simulate inefficient market prices
# Inefficient market returns are an AR(1) process
phi = 0.5
noise = np.random.normal(0, 0.01, len(inefficient_df))
inefficient_returns = np.zeros(len(inefficient_df))

for t in range(1, len(inefficient_df)):
    inefficient_returns[t] = phi * inefficient_returns[t - 1] + noise[t]

inefficient_prices = 100 * (1 + inefficient_returns).cumprod()
inefficient_df['price'] = inefficient_prices

# Simulate an evolutionary market, which slips in and out of inefficient regimes
regime_lengths = np.random.randint(12, 24, len(inefficient_df))
evolutionary_returns = np.zeros(len(inefficient_df))
i = 0
while i < len(evolutionary_returns):
    # Simulate an efficient regime
    regime_length = regime_lengths[i]
    evolutionary_returns[i:i + regime_length] = efficient_returns[i:i + regime_length]
    i = min(i + regime_length, len(evolutionary_returns))

    if i >= len(evolutionary_returns):
        break

    # Simulate an inefficient regime
    regime_length = min(regime_lengths[i], len(evolutionary_returns) - i)
    evolutionary_returns[i:i + regime_length] = inefficient_returns[i:i + regime_length]
    i += regime_length

evolutionary_prices = 100 * (1 + evolutionary_returns).cumprod()
evolutionary_df['price'] = evolutionary_prices

efficient_df.to_parquet('../data/00-simulated_data/efficient_market_prices.parquet')
inefficient_df.to_parquet('../data/00-simulated_data/inefficient_market_prices.parquet')
evolutionary_df.to_parquet('../data/00-simulated_data/evolutionary_market_prices.parquet')

# Plot the simulated data
plt.figure(figsize=(12, 6))
plt.plot(efficient_df['date'], efficient_df['price'], label='Efficient Market')
plt.plot(inefficient_df['date'], inefficient_df['price'], label='Inefficient Market')
plt.plot(evolutionary_df['date'], evolutionary_df['price'], label='Evolutionary Market')
plt.xlabel('Date')
plt.ylabel('Price')
plt.title('Simulated Market Prices')
plt.legend()
plt.savefig('../data/00-simulated_data/simulated_market_prices.png')

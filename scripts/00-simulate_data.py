#### Preamble ####
# Purpose: Simulates a dataset of efficient and inefficient market returns
# Author: Aman Rana
# Date: 22 November 2024
# Contact: aman.rana@mail.utoronto.ca
# License: MIT
# Pre-requisites: 
  # - `pandas` must be installed (pip install pandas)
  # - `numpy` must be installed (pip install numpy)
  # - `pyarrow` must be installed (pip install pyarrow)

#### Workspace setup ####
import pandas as pd
import numpy as np
np.random.seed(304)


#### Simulate data ####
# We will simulate two instances of a timeseries of returns from 1927 to 2024
# The first timeseries will be returns in an efficient market, where prices are a random walk
# The second timeseries will be returns in an inefficient market, where returns are influenced by a random walk

efficient_df = pd.DataFrame()
efficient_df['date'] = pd.date_range(start='1/1/1927', end='22/11/2024', freq='M')
inefficient_df = efficient_df.copy()

# Simulate efficient market prices
# Efficient market returns are random, making price a random walk
efficient_returns = np.random.normal(0, 0.01, len(efficient_df))  # Small returns with standard deviation of 1%
efficient_prices = 100 * (1 + efficient_returns).cumprod()
efficient_df['price'] = efficient_prices

# Simulate inefficient market prices
# Inefficient market returns are influenced by trends in the random walk
inefficient_returns = np.random.normal(0, 0.01, len(inefficient_df)) + 0.005  # Add a bias for trending returns
inefficient_prices = 100 * (1 + inefficient_returns).cumprod()
inefficient_df['price'] = inefficient_prices

efficient_df.to_parquet('data/00-simulated_data/efficient_market_prices.parquet')
inefficient_df.to_parquet('data/00-simulated_data/inefficient_market_prices.parquet')
#### Preamble ####
# Purpose: Tests SP500 data for nan values. Generates visual plots to check for any anomalies in market and Value Spread
# data.
# Author: Aman Rana
# Date: 23 November 2024
# Contact: aman.rana@mail.utoronto.ca
# License: MIT
# Pre-requisites:
#   - `pandas` must be installed (pip install pandas)
#   - `matplotlib` must be installed (pip install matplotlib)

#### Workspace setup ####
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#### Test data ####
sp500 = pd.read_parquet('../data/02-analysis_data/sp500.parquet')
assert sp500['Log Return'].isnull().values.any() == False, "Data contains nan values"

value_spread = pd.read_parquet('../data/02-analysis_data/value_spread.parquet')

assert value_spread['Value Spread'].isnull().values.any() == False, "Data contains nan values"

#### Visual plots ####
plt.figure(figsize=(10, 5))
plt.plot(sp500['Date'], sp500['Adj Close'])
plt.title('SP500 Price Data')
plt.xlabel('Date')
plt.ylabel('Log Price')
plt.savefig('../data/03-analysis_data_visuals/sp500_price.png')
plt.close()

# Plot market data
plt.figure(figsize=(10, 5))
plt.plot(sp500['Date'], np.log(sp500['Adj Close']))
plt.title('SP500 Log Price Data')
plt.xlabel('Date')
plt.ylabel('Log Price')
plt.savefig('../data/03-analysis_data_visuals/sp500_log_price.png')
plt.close()

#Plot a distribution of Log Returns
plt.hist(sp500['Log Return'], bins=100)
plt.title('SP500 Log Return Distribution')
plt.xlabel('Log Return')
plt.ylabel('Frequency')
plt.savefig('../data/03-analysis_data_visuals/sp500_log_return.png')
plt.close()

# Plot Value Spread
plt.figure(figsize=(10, 5))
plt.plot(value_spread['Date'], value_spread['Value Spread'])
plt.title('Value Spread')
plt.xlabel('Date')
plt.ylabel('Value Spread')
plt.savefig('../data/03-analysis_data_visuals/value_spread.png')
plt.close()

#Histogram of Value Spread
plt.hist(value_spread['Value Spread'], bins=100)
plt.title('Value Spread Distribution')
plt.xlabel('Value Spread')
plt.ylabel('Frequency')
plt.savefig('../data/03-analysis_data_visuals/value_spread_hist.png')
plt.close()


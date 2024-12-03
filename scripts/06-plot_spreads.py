#### Preamble ####
# Purpose: Plots the Value Spread and Market Inefficiency timeseries
# Author: Aman Rana
# Date: 24 November 2024
# Contact: aman.rana@mail.utoronto.ca
# License: MIT
# Pre-requisites:
#   - `pandas` must be installed (pip install pandas)
#   - `matplotlib` must be installed (pip install matplotlib)

#### Workspace setup ####

import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.stattools import coint
from scipy.stats import spearmanr

value_inefficiency_df = pd.read_parquet('../data/02-analysis_data/efficiency_and_value.parquet')
value_inefficiency_df.set_index('Date', inplace=True)
value_inefficiency_df = value_inefficiency_df.dropna()

#Plot Value Spread vs Market Efficiency
fig, ax1 = plt.subplots(figsize=(14, 7))
color = 'tab:red'
ax1.set_xlabel('Date')
ax1.set_ylabel('Market Inefficiency', color=color)
ax1.plot(value_inefficiency_df['Market Inefficiency'], color=color)
ax1.tick_params(axis='y', labelcolor=color)
ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
color = 'tab:blue'
ax2.set_ylabel('Value Spread', color=color)  # we already handled the x-label with ax1
ax2.plot(value_inefficiency_df['Value Spread'], color=color)
ax1.set_title('Timeseries of the Value Spread and Market Inefficiency')
plt.savefig('../figs/Value Spread and Market Inefficiency.png', dpi=300, bbox_inches='tight')
plt.close()

# Perform decomposition
value_result = seasonal_decompose(value_inefficiency_df['Value Spread'], model="additive", period=4*12)
eff_result = seasonal_decompose(value_inefficiency_df['Market Inefficiency'], model="additive", period=4*12)
#TODO: Ask Charles about the seasonality here.

#ADF Test on 'Market Inefficiency'
result = adfuller(value_inefficiency_df['Market Inefficiency'])
print(f'ADF p-value: {result[1]}')

#Engle-Granger Cointegration Test
result = coint(value_inefficiency_df['Market Inefficiency'],
               value_inefficiency_df['Value Spread'].diff().fillna(0))
print(f'Engle-Granger p-value: {result[1]}')

#Spearman Correlation
last_decade_df = value_inefficiency_df.loc['2009-01-01':].rolling(window=60).mean().dropna()
result = spearmanr(last_decade_df['Market Inefficiency'], last_decade_df['Value Spread'])
print(f'Spearman Correlation: {result.correlation}')

#Plot Value Spread vs Market Efficiency
fig, ax1 = plt.subplots(figsize=(14, 7))
color = 'tab:red'
ax1.set_xlabel('Date')
ax1.set_ylabel('Market Inefficiency', color=color)
ax1.plot(eff_result.trend, color=color)
ax1.tick_params(axis='y', labelcolor=color)
ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
color = 'tab:blue'
ax2.set_ylabel('Value Spread', color=color)  # we already handled the x-label with ax1
ax2.plot(value_result.trend, color=color)
ax1.set_title('Timeseries of the Value Spread and Market Inefficiency')
plt.savefig('../figs/Trends of Value Spread and Market Inefficiency.png', dpi=300, bbox_inches='tight')
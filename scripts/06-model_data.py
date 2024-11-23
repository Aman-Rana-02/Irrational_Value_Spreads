#### Preamble ####
# Purpose:
# Author: Aman Rana
# Date: 23 November 2024
# Contact: aman.rana@mail.utoronto.ca
# License: MIT
# Pre-requisites:


#### Workspace setup ####
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from utils.utils import robustness_regression, spot_market_inefficiency

#### Read data ####

spy_df = pd.read_parquet('../data/02-analysis_data/sp500.parquet')

### Model data ####
return_window = 36
for i in range(0, return_window+1):
    spy_df[f'Log Return t={i}'] = spy_df['Log Return'].shift(return_window-i)

spy_df[f'Log Return t={0}'] = 0
spy_df = spy_df.dropna()
for t in range(0, 37):
    spy_df[f'Cumulative Log Return {t}'] = spy_df.loc[:, f'Log Return t={0}':f'Log Return t={t}'].sum(axis=1)

all_time_regression_results = robustness_regression(spy_df)
all_time_market_inefficiency = spot_market_inefficiency(all_time_regression_results)

#Plot all time market inefficiency
plt.figure(figsize=(10, 5))
plt.plot(all_time_regression_results.index, all_time_regression_results['beta'])
plt.scatter(all_time_regression_results.index, all_time_regression_results['beta'])
plt.title('Beta vs Window Size')
plt.xlabel('Window Size')
plt.ylabel('Beta')
plt.savefig('../figs/SP500_Beta_vs_Window_Size.png')

### For each month get market efficiency ###
window_size = 5*12
start_index = 0
while start_index + window_size <= len(spy_df):
    # Define the window range
    window_data = spy_df[start_index:start_index + window_size]
    regression_results = robustness_regression(window_data)
    try:
        market_inefficiency = spot_market_inefficiency(regression_results)
    except:
        market_inefficiency = np.nan
    spy_df.loc[start_index + window_size, 'Market Inefficiency'] = market_inefficiency
    start_index += 1

value_spread = pd.read_parquet('../data/02-analysis_data/value_spread.parquet')

value_inefficiency_df = pd.merge(spy_df[['Date', 'Market Inefficiency']], value_spread, on='Date', how='inner')
value_inefficiency_df.to_parquet('../data/02-analysis_data/efficiency_and_value.parquet')
value_inefficiency_df.set_index('Date', inplace=True)
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
plt.savefig('../figs/Value_Spreads_and_Inefficiency.png')
#### Save model ####




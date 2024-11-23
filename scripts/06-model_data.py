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
from utils.utils import robustness_regression, spot_market_efficiency

#### Read data ####

spy_df = pd.read_parquet('../data/02-analysis_data/sp500.parquet')

### Model data ####
return_window = 36
for i in range(1, return_window+1):
    spy_df[f'Log Return t={i}'] = spy_df['Log Return'].shift(return_window-i)

spy_df[f'Log Return t={0}'] = 0

for t in range(0, 37):
    spy_df[f'Cumulative Log Return {t}'] = spy_df.loc[:, f'Log Return t={0}':f'Log Return t={t}'].sum(axis=1)

### For each month get market efficiency ###
window_size = 5*12
start_index = 0
while start_index + window_size <= len(spy_df):
    # Define the window range
    window_data = spy_df[start_index:start_index + window_size]
    regression_results = robustness_regression(window_data)
    market_efficiency = spot_market_efficiency(regression_results)
    spy_df.loc[start_index + window_size, 'Market Efficiency'] = market_efficiency
    start_index += 1

value_spread = pd.read_parquet('../data/02-analysis_data/value_spread.parquet')

regression_df = pd.merge(spy_df[['Date', 'Market Efficiency']], value_spread, on='Date', how='inner')

#### Save model ####




#### Preamble ####
# Purpose:
# Author: Aman Rana
# Date: 23 November 2024
# Contact: aman.rana@mail.utoronto.ca
# License: MIT
# Pre-requisites:


#### Workspace setup ####
import pandas as pd
import warnings
import matplotlib.pyplot as plt
from utils.utils import (robustness_regression, spot_market_inefficiency, rolling_robustness_regressions,
                         get_return_windows, plot_market_inefficiency, plot_rolling_market_inefficiency)
warnings.filterwarnings("ignore", category=pd.errors.SettingWithCopyWarning)
#### Read data ####

spy_df = pd.read_parquet('../data/02-analysis_data/sp500.parquet')
efficient_market_df = pd.read_parquet('../data/00-simulated_data/efficient_market_prices.parquet')
inefficient_market_df = pd.read_parquet('../data/00-simulated_data/inefficient_market_prices.parquet')
evolutionary_market_df = pd.read_parquet('../data/00-simulated_data/evolutionary_market_prices.parquet')

# 1950 onwards
spy_df = spy_df[spy_df['Date'] >= '1950-01-01']

### Model data ####
spy_df = get_return_windows(spy_df)
all_time_regression_results = robustness_regression(spy_df)
all_time_market_inefficiency = spot_market_inefficiency(all_time_regression_results)

efficient_market_df = get_return_windows(efficient_market_df)
efficient_market_regression_results = robustness_regression(efficient_market_df)
efficient_market_market_inefficiency = spot_market_inefficiency(efficient_market_regression_results)

inefficient_market_df = get_return_windows(inefficient_market_df)
inefficient_market_regression_results = robustness_regression(inefficient_market_df)
inefficient_market_market_inefficiency = spot_market_inefficiency(inefficient_market_regression_results)

evolutionary_market_df = get_return_windows(evolutionary_market_df)
evolutionary_market_regression_results = robustness_regression(evolutionary_market_df)
evolutionary_market_market_inefficiency = spot_market_inefficiency(evolutionary_market_regression_results)

# Plot market inefficiency
plot_market_inefficiency(all_time_regression_results, 'SP500 Market Inefficiency')
plot_market_inefficiency(efficient_market_regression_results, 'Simulated Efficient Market Inefficiency')
plot_market_inefficiency(inefficient_market_regression_results, 'Simulated Inefficient Market Inefficiency')
plot_market_inefficiency(evolutionary_market_regression_results, 'Simulated Evolutionary Market Inefficiency')

### For each month get market efficiency ###
spy_df = rolling_robustness_regressions(spy_df, window_size=5 * 12)
efficient_market_df = rolling_robustness_regressions(efficient_market_df, window_size=5*12)
inefficient_market_df = rolling_robustness_regressions(inefficient_market_df, window_size=5*12)
evolutionary_market_df = rolling_robustness_regressions(evolutionary_market_df, window_size=5*12)

# Plot rolling market inefficiency
plot_rolling_market_inefficiency(spy_df, 'SP500 Rolling Market Inefficiency')
plot_rolling_market_inefficiency(efficient_market_df, 'Simulated Efficient Market Rolling Inefficiency')
plot_rolling_market_inefficiency(inefficient_market_df, 'Simulated Inefficient Market Rolling Inefficiency')

#Special Case of Evolutionary Market
plt.figure(figsize=(10, 5))

plt.plot(evolutionary_market_df['Date'], evolutionary_market_df['Market Inefficiency'], label='Market Inefficiency')

for i in range(len(evolutionary_market_df) - 1):
    if evolutionary_market_df['Efficiency State'].iloc[i] == 0:
        plt.axvspan(
            evolutionary_market_df['Date'].iloc[i],
            evolutionary_market_df['Date'].iloc[i + 1],
            color='grey',
            alpha=0.5
        )
plt.title('Simulated Evolutionary Market Rolling Inefficiency')
plt.xlabel('Date')
plt.ylabel('Market Inefficiency')
plt.legend()
plt.savefig('../figs/Simulated Evolutionary Market Rolling Inefficiency.png')

value_spread = pd.read_parquet('../data/02-analysis_data/value_spread.parquet')
value_inefficiency_df = pd.merge(spy_df[['Date', 'Market Inefficiency']], value_spread, on='Date', how='inner')
value_inefficiency_df.to_parquet('../data/02-analysis_data/efficiency_and_value.parquet')

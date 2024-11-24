import pandas as pd
import matplotlib.pyplot as plt

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
plt.savefig('../figs/Value Spread and Market Inefficiency.png')
import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt

def get_return_windows(df, return_window = 36):
    for i in range(0, return_window + 1):
        # In the preceding T=return_window period, returns were Eff/Ineff
        # df[f'Log Return t={i}'] = df['Log Return'].shift(return_window - i)

        #TODO: Speak to Charles.
        # In the forward T=return_window period, returns were Eff/Ineff
        df[f'Log Return t={i}'] = df['Log Return'].shift(-i)
    df[f'Log Return t={0}'] = 0
    df = df.dropna()
    for t in range(0, 37):
        df[f'Cumulative Log Return {t}'] = df.loc[:, f'Log Return t={0}':f'Log Return t={t}'].sum(axis=1)
    return df

def plot_market_inefficiency(df, title):
    plt.figure(figsize=(10, 5))
    plt.plot(df.index, df['beta'])
    plt.scatter(df.index, df['beta'])
    plt.title(title)
    plt.xlabel('Window Size')
    plt.ylabel('Beta')
    plt.savefig(f'../figs/{title}.png')

def plot_rolling_market_inefficiency(df, title):
    plt.figure(figsize=(10, 5))
    plt.plot(df['Date'], df['Market Inefficiency'])
    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel('Market Inefficiency')
    plt.savefig(f'../figs/{title}.png')

def robustness_regression(df, lag_range=(0, 36)):
    params = []
    for i in range(lag_range[0], lag_range[1]+1):
        X = df[f'Cumulative Log Return {i}'].values
        y = df[f'Cumulative Log Return {lag_range[1]}'].values

        X = sm.add_constant(X)

        model = sm.OLS(y, X)
        results = model.fit()
        params.append((i, results.params[1], results.bse[1], results.rsquared))

    return pd.DataFrame(params, columns=['i', 'beta', 'se', 'r2']).set_index('i')

def spot_market_inefficiency(regression_results_df):
    # Initialize the total sum of squared deviations
    total_sum_squares = 0
    n_observed = 0
    for index, beta, se in zip(regression_results_df.index, regression_results_df['beta'], regression_results_df['se']):
        if index == regression_results_df.index[0]:
            continue
        deviation = beta - 1
        # squared_deviation = abs(deviation / se)
        if se == 0 or abs(deviation / se) <= 1.96:
            squared_deviation = 0
        else:
            squared_deviation = deviation ** 2

        total_sum_squares += squared_deviation
        n_observed += 1

    # Return the total sum of squares
    return total_sum_squares

def rolling_robustness_regressions(df, window_size=5*12):
    start_index = 0
    while start_index + window_size <= len(df):
        print('Progress: ', start_index / len(df), end='\r')
        # Define the window range
        window_data = df[start_index:start_index + window_size]
        regression_results = robustness_regression(window_data)
        market_inefficiency = spot_market_inefficiency(regression_results)
        window_last_date = window_data['Date'].iloc[-1]
        # Set the market inefficiency value in the date in df
        df.loc[df['Date'] == window_last_date, 'Market Inefficiency'] = market_inefficiency
        start_index += 1
    return df
#### Preamble ####
# Purpose: Provide utility functions for the analysis of market inefficiency.
# Author: Aman Rana
# Date: 23 November 2024
# Contact: aman.rana@mail.utoronto.ca
# License: MIT
# Pre-requisites:
#   - `pandas` must be installed (pip install pandas)
#   - `matplotlib` must be installed (pip install matplotlib)
#   - `statsmodels` must be installed (pip install statsmodels)

#### Workspace setup ####
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt

#### Utility functions ####
def get_return_windows(df, return_window = 36):
    '''
    Expects a dataframe with a 'Log Return' column.
    Generates columns for the cumulative log returns for each window size.
    :param df:
    :param return_window:
    :return:
    '''
    for i in range(0, return_window + 1):
        df[f'Log Return t={i}'] = df['Log Return'].shift(-i)

    df[f'Log Return t={0}'] = 0
    df = df.dropna()
    for t in range(0, 37):
        df[f'Cumulative Log Return {t}'] = df.loc[:, f'Log Return t={0}':f'Log Return t={t}'].sum(axis=1)

    for i in range(0, return_window + 1):
        df = df.drop(columns=[f'Log Return t={i}'])

    return df

def plot_market_inefficiency(df, title):
    '''
    Plots the market inefficiency over time.
    Expects a dataframe with a 'Market Inefficiency' column.
    :return:
    '''
    plt.figure(figsize=(10, 5))
    plt.plot(df.index, df['beta'])
    plt.scatter(df.index, df['beta'])
    plt.title(title)
    plt.xlabel('Window Size')
    plt.ylabel('Beta')
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)

    plt.savefig(f'../figs/{title}.png', dpi=300, bbox_inches='tight')


def plot_spot_market_inefficiency_score(df, title):
    '''
    Plots the market inefficiency over time with additional visual aids.
    Expects a dataframe with a 'beta' column.
    :param df: DataFrame with 'beta' column
    :param title: Title for the plot
    :return: None
    '''
    plt.figure(figsize=(10, 5))
    plt.plot(df.index, df['beta'], label='Beta', marker='o')

    # Add dotted line at Beta=1
    plt.axhline(y=1, color='black', linestyle='--', linewidth=1, label='Beta = 1')

    # Add red vertical lines connecting each point to Beta=1
    for idx, beta in zip(df.index, df['beta']):
        # Skip the first point
        if idx == df.index[0]:
            continue
        plt.plot([idx, idx], [beta, 1], color='red', linestyle='-', linewidth=1)

    # Add labels and title
    plt.title(title)
    plt.xlabel('Window Size')
    plt.ylabel('Beta')
    plt.legend()
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)

    # Save the plot as a PNG file
    plt.savefig(f'../figs/{title}.png', dpi=300, bbox_inches='tight')
    plt.show()

def plot_rolling_market_inefficiency(df, title):
    '''
    Plots the rolling market inefficiency over time.
    Expects a dataframe with a 'Market Inefficiency' column.
    :return:
    '''
    plt.figure(figsize=(10, 5))
    plt.plot(df['Date'], df['Market Inefficiency'])
    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel('Market Inefficiency')
    plt.savefig(f'../figs/{title}.png', dpi=300, bbox_inches='tight')

def robustness_regression(df, lag_range=(0, 36)):
    '''
    Expects a dataframe with columns for cumulative log returns. E.g as generated by get_return_windows.
    returns the results from a regression of the cumulative log returns.
    :return: A pandas dataframe with the robustness regression results.
    '''
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
    '''
    Expects a dataframe with robustness regression results, columns for beta and se. E.g as generated by robustness_regression.
    Where the index is the lag value.
    Returns the total sum of squared deviations from the null hypothesis (B=1).
    Does not include the first row since B=0 by default.
    Does not include deviations not statistically different from 1 at the 95% confidence level.
    :return:
    '''
    # Initialize the total sum of squared deviations
    total_sum_squares = 0
    n_observed = 0
    for index, beta, se in zip(regression_results_df.index, regression_results_df['beta'], regression_results_df['se']):
        if index == regression_results_df.index[0]:
            continue
        deviation = beta - 1
        # squared_deviation = abs(deviation / se)
        # if se == 0 or abs(deviation / se) <= 1.96:
        #     squared_deviation = 0
        # else:
        squared_deviation = deviation ** 2

        total_sum_squares += squared_deviation
        n_observed += 1

    # Return the total sum of squares
    return total_sum_squares

def rolling_robustness_regressions(df, window_size=5*12):
    '''
    Expects a dataframe with columns for cumulative log returns. E.g as generated by get_return_windows.
    Returns the dataframe with a column for market inefficiency.
    Does rolling robustness regressions over the window size.
    :return: A pandas dataframe with the market inefficiency values.
    '''
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
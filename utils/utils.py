import pandas as pd
import numpy as np
import statsmodels.api as sm

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

    # Loop through each data point in the df
    for index, beta, se in zip(regression_results_df.index, regression_results_df['beta'], regression_results_df['se']):
        # drop the first value
        if index == regression_results_df.index[0] or index == regression_results_df.index[-1]:
            continue
        # Calculate the squared deviation
        deviation = beta - 1
        squared_deviation = (deviation / se) ** 2

        # Add the squared deviation to the total sum
        total_sum_squares += squared_deviation

    # Return the total sum of squares
    return total_sum_squares

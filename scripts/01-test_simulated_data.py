#### Preamble ####
# Purpose: Tests the structure and validity of the simulated efficient, inefficient, and evolutionary
# market datasets
# Author: Aman Rana
# Date: 23 November 2024
# Contact: aman.rana@mail.utoronto.ca
# License: MIT
# Pre-requisites:
  # - `pandas` must be installed (pip install pandas)
    # - `numpy` must be installed (pip install numpy)
    # - `arch` must be installed (pip install arch)
  # - 00-simulate_data.py must have been run

#### Workspace setup ####
import pandas as pd
import numpy as np
from arch.unitroot import VarianceRatio

efficient_df = pd.read_parquet('../data/00-simulated_data/efficient_market_prices.parquet')
inefficient_df = pd.read_parquet('../data/00-simulated_data/inefficient_market_prices.parquet')
evolutionary_df = pd.read_parquet('../data/00-simulated_data/evolutionary_market_prices.parquet')

efficient_df['log_price'] = np.log(efficient_df['price'])
inefficient_df['log_price'] = np.log(inefficient_df['price'])
evolutionary_df['log_price'] = np.log(evolutionary_df['price'])

#### Test Market Efficiency with the Variance Ratio Test ####
VarianceRatioTest = VarianceRatio(efficient_df['log_price'], lags=12)
print("Efficient Market Variance Ratio Test:")
print(VarianceRatioTest.summary())
print("We do not reject the null hypothesis of a random walk in the efficient market. \n")

VarianceRatioTest = VarianceRatio(inefficient_df['log_price'], lags=12)
print("Inefficient Market Variance Ratio Test:")
print(VarianceRatioTest.summary())
print("We reject the null hypothesis of a random walk in the inefficient market. \n")

VarianceRatioTest = VarianceRatio(evolutionary_df['log_price'], lags=12)
print("Evolutionary Market Variance Ratio Test:")
print(VarianceRatioTest.summary())
print("We reject the null hypothesis of a random walk in the evolutionary market.")
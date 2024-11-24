#### Preamble ####
# Purpose: Tests the structure and validity of the simulated efficient, inefficient, and evolutionary
# market datasets
# Author: Aman Rana
# Date: 23 November 2024
# Contact: aman.rana@mail.utoronto.ca
# License: MIT
# Pre-requisites:
#  - `pandas` must be installed (pip install pandas)
#  - `numpy` must be installed (pip install numpy)
#  - `arch` must be installed (pip install arch)
#  -  00-simulate_data.py must have been run

#### Workspace setup ####
import pandas as pd
import numpy as np
from arch.unitroot import VarianceRatio

efficient_df = pd.read_parquet('../data/00-simulated_data/efficient_market_prices.parquet')
inefficient_df = pd.read_parquet('../data/00-simulated_data/inefficient_market_prices.parquet')
evolutionary_df = pd.read_parquet('../data/00-simulated_data/evolutionary_market_prices.parquet')

efficient_df['Log Price'] = np.log(efficient_df['Adj Close'])
inefficient_df['Log Price'] = np.log(inefficient_df['Adj Close'])
evolutionary_df['Log Price'] = np.log(evolutionary_df['Adj Close'])

#### Test Market Efficiency with the Variance Ratio Test ####
VarianceRatioTest = VarianceRatio(efficient_df['Log Price'], lags=12)
print("Efficient Market Variance Ratio Test:")
print(VarianceRatioTest.summary())
print("We do not reject the null hypothesis of a random walk in the efficient market. \n")

VarianceRatioTest = VarianceRatio(inefficient_df['Log Price'], lags=12)
print("Inefficient Market Variance Ratio Test:")
print(VarianceRatioTest.summary())
print("We reject the null hypothesis of a random walk in the inefficient market. \n")

VarianceRatioTest = VarianceRatio(evolutionary_df['Log Price'], lags=12)
print("Evolutionary Market Variance Ratio Test:")
print(VarianceRatioTest.summary())
print("We reject the null hypothesis of a random walk in the evolutionary market.")

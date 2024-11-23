#### Preamble ####
# Purpose: Cleans and formats the raw Yahoo Finance and Fama-French data
# Author: Aman Rana
# Date: 23 November 2023
# Contact: aman.rana@mail.utoronto.ca
# License: MIT
# Pre-requisites:
#   - `pandas` must be installed (pip install pandas)
#   - `numpy` must be installed (pip install numpy)
#   -  02-download_data.py must have been run
#   -  Fama-French 2x3 sorted Size (ME) and Value (Book-To-Market) Portfolios must be downloaded,
#      and the Value Weighted Average BE/ME must be manually extracted (Rows 4954 onwards from 6_Portfolios_2x3.csv
#      as of 23 November 2023)

#### Workspace setup ####
import pandas as pd
import numpy as np

#### Clean yfinance data ####
df = pd.read_csv('../data/01-raw_data/^GSPC.csv')
#Drop first two rows (ignoring the header)
df = df.drop([0,1]).reset_index(drop=True)
df.rename(columns={'Price': 'Date'}, inplace=True)
df['Date'] = pd.to_datetime(df['Date'])
df['Adj Close'] = pd.to_numeric(df['Adj Close'])
df.set_index('Date', inplace=True)
df.sort_index(inplace=True)
df = df.resample('M').last()
df.index = df.index + pd.DateOffset(days=1)
df = df.reset_index()
df['Log Return'] = np.log(df['Adj Close']).diff()
df = df[['Date', 'Adj Close', 'Log Return']]
df['Log Return'].fillna(0, inplace=True)
df.to_parquet('../data/02-analysis_data/sp500.parquet')

#### Clean Fama-French data and construct Value Spread ####
df = pd.read_csv('../data/01-raw_data/Value_Weight_Average_of_BE_ME.csv')
df['Date'] = pd.to_datetime(df['Date'], format='%Y%m')
df.sort_values('Date', inplace=True)
#The spread of BM of large caps, as per Asness (2024)
df['Value Spread'] = df['BIG HiBM'] / df['BIG LoBM']
df = df[['Date', 'Value Spread']]
df.to_parquet('../data/02-analysis_data/value_spread.parquet')
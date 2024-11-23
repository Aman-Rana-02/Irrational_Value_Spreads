#### Preamble ####
# Purpose: Downloads and saves SP500 market data from Yahoo Finance
# Author: Aman Rana
# Date: 23 November 2023
# Contact: aman.rana@mail.utoronto.ca
# License: MIT
# Pre-requisites:
#   - `yfinance` must be installed (pip install yfinance)

#### Workspace setup ####
import yfinance as yf

# Define the date range
start_date = '1926-07-01'
interval='1D'
ticker = '^GSPC'
data = yf.download(ticker, start=start_date, interval=interval)

filename = f'../data/01-raw_data/^GSPC.csv'

# Save the DataFrame to a CSV file
data.to_csv(filename, index=True)

print(f"Data saved to {filename}")

# Fama-French Value (Book-To-Market) Portfolio Returns are downloaded from the following link:
# https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html
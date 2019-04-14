# -*- coding: utf-8 -*-
"""Test_Dataset_Framework.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1_-14xhia99FuCKkyTalSEYvv77Uet4xv

# Test_Dataset_Framework

### Data
1. Company Financials
2. Company Stock Prices
"""

# DB Files for S&P 500 Companies
from google.colab import drive

# Files to process
do_file = "/content/gdrive/My Drive/Colab Notebooks/Data/Bondai/Test/do_file.txt"
done_file = "/content/gdrive/My Drive/Colab Notebooks/Data/Bondai/Test/done_file.txt"

# Reading the files
import pandas as pd
do_df = pd.read_csv("/content/gdrive/My Drive/Colab Notebooks/Data/Bondai/Test/do_file.txt", header=None, names=["Tickers"])
done_df = pd.read_csv("/content/gdrive/My Drive/Colab Notebooks/Data/Bondai/Test/done_file.txt", header=None, names=["Tickers"])

do_set = set(do_df["Tickers"].tolist())
done_set = set(done_df["Tickers"].tolist())

# URL Paths for Stockrow Website

stockrow_url_paths = {
    'company': 'https://stockrow.com/api/companies/',
    'annual': {
        'income-statement': '/financials.xlsx?dimension=MRY&section=Income%20Statement&sort=desc',
        'balance-sheet': '/financials.xlsx?dimension=MRY&section=Balance%20Sheet&sort=desc',
        'cashflow-statement': '/financials.xlsx?dimension=MRY&section=Cash%20Flow&sort=desc',
        'metrics': '/financials.xlsx?dimension=MRY&section=Metrics&sort=desc',
        'growth': '/financials.xlsx?dimension=MRY&section=Growth&sort=desc'
    } 
}

# Stockrow Downloader
import requests
def stockrow_download(ticker):
    income_statement = pd.read_excel(stockrow_url_paths['company'] + ticker + stockrow_url_paths['annual']["income-statement"], engine="xlrd")
    balance_sheet = pd.read_excel(stockrow_url_paths['company'] + ticker + stockrow_url_paths['annual']["balance-sheet"], engine="xlrd")
    cashflow_statement = pd.read_excel(stockrow_url_paths['company'] + ticker + stockrow_url_paths['annual']["cashflow-statement"], engine="xlrd")
    metrics = pd.read_excel(stockrow_url_paths['company'] + ticker + stockrow_url_paths['annual']["metrics"], engine="xlrd")
    growth = pd.read_excel(stockrow_url_paths['company'] + ticker + stockrow_url_paths['annual']["growth"], engine="xlrd")
    return income_statement, balance_sheet, cashflow_statement, metrics, growth

# Modified Get Yahoo Quotes Script by Brad Luicas

__author__ = "Brad Luicas"
__copyright__ = "Copyright 2017, Brad Lucas"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Brad Lucas"
__email__ = "brad@beaconhill.com"
__status__ = "Production"

import re
import sys
import time
import datetime
# import requests


def split_crumb_store(v):
    return v.split(':')[2].strip('"')


def find_crumb_store(lines):
    # Looking for
    # ,"CrumbStore":{"crumb":"9q.A4D1c.b9
    for l in lines:
        if re.findall(r'CrumbStore', l):
            return l
    print("Did not find CrumbStore")


def get_cookie_value(r):
    return {'B': r.cookies['B']}


def get_page_data(symbol):
    url = "https://finance.yahoo.com/quote/%s/?p=%s" % (symbol, symbol)
    r = requests.get(url)
    cookie = get_cookie_value(r)

    # Code to replace possible \u002F value
    # ,"CrumbStore":{"crumb":"FWP\u002F5EFll3U"
    # FWP\u002F5EFll3U
    lines = r.content.decode('unicode-escape').strip(). replace('}', '\n')
    return cookie, lines.split('\n')


def get_cookie_crumb(symbol):
    cookie, lines = get_page_data(symbol)
    crumb = split_crumb_store(find_crumb_store(lines))
    return cookie, crumb


def get_data(symbol, start_date, end_date, cookie, crumb):
    # filename = '%s.csv' % (symbol)
    url = "https://query1.finance.yahoo.com/v7/finance/download/%s?period1=%s&period2=%s&interval=1d&events=history&crumb=%s" % (symbol, start_date, end_date, crumb)
    response = requests.get(url, cookies=cookie)
    # with open (filename, 'wb') as handle:
    #     for block in response.iter_content(1024):
    #         handle.write(block)
    return response


def get_now_epoch():
    # @see https://www.linuxquestions.org/questions/programming-9/python-datetime-to-epoch-4175520007/#post5244109
    return int(time.time())


def download_quotes(symbol):
    start_date = 0
    end_date = get_now_epoch()
    cookie, crumb = get_cookie_crumb(symbol)
    historical_prices = get_data(symbol, start_date, end_date, cookie, crumb)
    return pd.read_csv(io.StringIO(historical_prices.content.decode('utf-8')))

import os
import io
def main():
    for ticker in do_set.copy():
        print("Downloading data for: " + ticker)
        income_statement, balance_sheet, cashflow_statement, metrics, growth = stockrow_download(ticker)
        historical_prices = download_quotes(ticker)
        with pd.ExcelWriter('/content/gdrive/My Drive/Colab Notebooks/Data/Bondai/Test/' + ticker + '.xlsx') as writer:
            historical_prices.to_excel(writer, sheet_name="historical_prices")
            balance_sheet.to_excel(writer, sheet_name="balance_sheet")
            income_statement.to_excel(writer, sheet_name="income_statement")
            cashflow_statement.to_excel(writer, sheet_name="cashflow_statement")
            metrics.to_excel(writer, sheet_name="metrics")
            growth.to_excel(writer, sheet_name="growth")
            
        done_set.add(ticker)
        do_set.discard(ticker)
        pd.DataFrame(list(done_list)).to_csv("/content/gdrive/My Drive/Colab Notebooks/Data/Bondai/Test/do_file.txt", header=None, index=False)
        pd.DataFrame(list(do_list)).to_csv("/content/gdrive/My Drive/Colab Notebooks/Data/Bondai/Test/do_file.txt", header=None, index=False)

main()

income_statement, balance_sheet, cashflow_statement, metrics, growth = stockrow_download("AAPL")

# df = pd.ExcelFile("https://stockrow.com/api/companies/AAPL/financials.xlsx?dimension=MRQ&section=Balance%20Sheet&sort=desc", engine="xlrd")
# pd.read_excel(df)
import io
historical_prices = download_quotes("AAPL")
df = pd.read_csv(io.StringIO(historical_prices.content.decode('utf-8')))

income_statement

with pd.ExcelWriter('/content/gdrive/My Drive/Colab Notebooks/Data/Bondai/Test/multi.xlsx') as writer:
    pd.read_csv(io.StringIO(historical_prices.content.decode('utf-8'))).to_excel(writer, sheet_name="stocks")
    balance_sheet.to_excel(writer, sheet_name="weather")

pd.DataFrame(list(done_list)).to_csv("/content/gdrive/My Drive/Colab Notebooks/Data/Bondai/Test/test.txt", header=None, index=False)

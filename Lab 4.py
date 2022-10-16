#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 12 17:50:48 2022

@author: brettcarey
"""

import json
import requests
import pandas
from datetime import datetime

#Get user input for stock ticker
stock = input("Stock: ")

#Initialize loop to allow for exception handling
flag = 0
while flag == 0:
    try:
        #Call the API to get the info
        url1 = 'https://query1.finance.yahoo.com/v7/finance/quote'
        querystring = {"symbols": stock}
        header_var = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        response = requests.request("GET",url1,headers=header_var,params=querystring)
        stock_json = response.json()
        long_name = stock_json['quoteResponse']['result'][0]['longName']
        current_price = stock_json['quoteResponse']['result'][0]['regularMarketPrice']
        url2="https://query1.finance.yahoo.com/v10/finance/quoteSummary/"
        query_str = {"symbol": stock, "modules":"defaultKeyStatistics"}
        response2 = requests.request("GET",url2, headers=header_var,params=query_str)
        stock_json2 = response2.json()
        profit_margins = stock_json2['quoteSummary']['result'][0]['defaultKeyStatistics']['profitMargins']['fmt']
        query_str3 = {"symbol": stock, "modules":"financialData"}
        response3 = requests.request("GET",url2, headers=header_var,params=query_str3)
        stock_json3 = response3.json()
        cash_on_hand = stock_json3['quoteSummary']['result'][0]['financialData']['totalCash']['fmt']
        target_mean_price = stock_json3['quoteSummary']['result'][0]['financialData']['targetMeanPrice']['fmt']
        #Change the loop condition so the loop is exited
        flag = 1
    except:
        #Give the user another chance to input in case of exception
        print("Try again")
        stock = input("Stock: ")
#Display the info
print("Name Ticker:", stock)
print("Full Name of the Stock:", long_name)
print("Current Price:", current_price)
print("Target Mean Price:", target_mean_price)
print("Cash on Hand:", cash_on_hand)
print("Profit Margins:", profit_margins)
#Get the date
today=datetime.today().strftime('%Y-%m-%d')
#Create the JSON file
stock_info = {"Name Ticker": stock, 
              "Full Name of the Stock": long_name,
              "Current Price": current_price, 
              "Target Mean Price": target_mean_price, 
              "Cash on Hand": cash_on_hand,
              "Profit Margins": profit_margins,
              "Date Pulled": today
              }
stock_info_json = json.dumps(stock_info, indent=7)
with open('stock_info.json', 'w') as f:
    f.write(stock_info_json)

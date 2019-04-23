import requests, json
#from Quandl import Quandl
import quandl
import pandas as pd
from pathlib import Path, PureWindowsPath
import os

import bitfinex

#Everytime check which OS the program should be runned. And modify the code.
DIR_FILE_Windows = "D:\\Projects\\PythonApps\\CryptoPrediction\\cryptoData\\currentData"
DIR_FILE_MAC = "./cryptoData/currentData"
path_full = "D:\\Projects\\PythonApps\\CryptoPrediction\\cryptoData\\currentData\\BITSTAMPEUR.csv"

auth_tok = '9MGsFkdirR5KaUbd9usn'


# The data can be selected from time: 2018-01-13 (oldest data from Quandl API about Bitcoin = EUR)
def get_bitcoin_data(start_time, end_time):
    if os.path.isfile(path_full):
        new_df = pd.read_csv(path_full, index_col='Date')
    else:
        new_df = quandl.get("BCHARTS/BITSTAMPEUR", authtoken=auth_tok, start_date=start_time, end_date=end_time)
        save_to_file(new_df)

    new_df = modify_data(new_df)
    return new_df
    #return data


#Saving the fetched dataframe into a CSV file. For analysis purpose.
def save_to_file(df):
    #try:
    df.to_csv(os.path.join(DIR_FILE_Windows, "BITSTAMPEUR.csv"), sep=",", index=True)
    #catch():
    return print("The data has been saved into file. ")


# Creating a new dataframe with selected columns. There is two way to do this.
def modify_data(df):
    new_df = df[['Open', 'High', 'Low', 'Close', 'Volume (BTC)']].copy()
    return new_df


# === Main section for testing purpose
# df = pd.DataFrame()
# save_to_file(df)
# modify_data(df)

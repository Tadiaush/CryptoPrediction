import pandas as pd
import datetime
from pathlib import Path, PureWindowsPath
import os

#import bitfinex

# Everytime check which OS the program should be runned. And modify the code.
DIR_FILE_Windows = "D:\\Projects\\PythonApps\\CryptoPrediction\\cryptoData\\currentData"
DIR_FILE_MAC = "./cryptoData/currentData"
path_full = "D:\\Projects\\PythonApps\\CryptoPrediction\\cryptoData\\allData\\bitstampUSD_1-min_data_2012-01-01_to_2019-03-13.csv"

auth_tok = '9MGsFkdirR5KaUbd9usn'


# Saving the fetched dataframe into a CSV file. For analysis purpose.
def save_to_file(df):
    # try:
    #df.to_csv(os.path.join(DIR_FILE_Windows, "BITSTAMPEUR.csv"), sep=",", index=True)
    df.to_csv(os.path.join(DIR_FILE_Windows, "COINAPI_BTC_EUR.csv"), sep=",", index=True)
    # catch():
    return print("The data has been saved into file. ")


# Creating a new dataframe with selected columns. There is two way to do this.
def modify_data(df):
    new_df = df[['Open', 'High', 'Low', 'Close', 'Volume (BTC)']].copy()
    return new_df

# def get_data_coinapi():
#     months = ['2018-01-01', '2018-02-01', '2018-03-01', '2018-04-01', '2018-05-01', '2018-06-01']
#     months_end = ['2018-01-30', '2018-02-27', '2018-03-30', '2018-04-30', '2018-05-30', '2018-06-30']
#     headers = {'X-CoinAPI-Key' : '3E795BD1-7740-4839-80FD-F7CEAE8066E9'}
#     i = 0
#     main_df = pd.DataFrame()
#     for month in months:
#         url = f'https://rest.coinapi.io/v1/ohlcv/BTC/EUR/history?period_id=1HRS&time_start={month}T00:00:00&time_end={months_end[i]}T00:00:00&limit=720'
#         #url = f'https://rest.coinapi.io/v1/ohlcv/BTC/EUR/history?period_id=1HRS&time_start=2018-01-01T00:00:00&time_end=2018-01-02T00:00:00'
#
#         i += 1
#         response = requests.get(url, headers=headers).json()
#         print(response)
#         #data = json.loads(response)
#         data = pd.DataFrame.from_dict(response, orient='columns')
#         #print(data)
#         main_df = pd.concat([main_df, data])
#     return main_df
#

def import_data():
    df = pd.read_csv(path_full)
    print(df.dtypes)
    return df

def clear_data(df):
    #df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='s')
    #print(df)
    # vienas menuo - 2018-05-01 = 2018-06-01
    #new_df = df.loc[(df['Timestamp'] > 1525176000) & (df['Timestamp'] < 1527811200)]
    new_df = df.loc[(df['Timestamp'] > 1514808000) & (df['Timestamp'] < 1546344000)]
    #print(new_df)
    return new_df



# === Main section for testing purpose
# df = pd.DataFrame()
# save_to_file(df)
# modify_data(df)
#df = import_data()
#clear_data(df)
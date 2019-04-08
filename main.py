import os
from datetime import datetime
import pandas as pd
from cryptoData import getData

DIR_PATH = os.path.dirname(os.path.abspath(__file__))
DIR_DATA = "~/programming/Python/CryptoPrediction/"
DIR_CURRENT = "./cryptoData/currentData/"
DIR_ARCHIVE = "./cryptoData/archive/"


def modify_df(df):
    # new_df = df.drop(columns="time" "open" "high")
    new_df = df[['close', 'volume']]
    return new_df


# def preprocess_df(df):
#     for col in df.columns:
#         if

# data, last_unix = getData.fetch_data()
# modified_data = modify_df(data)
# print(modified_data)R
# df = getData.fetch_data()
#df, file = getData.save_to_file()
df_new = pd.DataFrame(pd.read_csv('~/programming/Python/CryptoPrediction/cryptoData/currentData/BCHUSD_2019-04-08_19:08:00.csv',
                     index_col=['dtime']))
df_new_2 = pd.DataFrame(pd.read_csv('~/programming/Python/CryptoPrediction/cryptoData/currentData/BCHUSD_2019-04-08_19:20:00.csv',
                     index_col=['dtime']))
full_df = pd.DataFrame(pd.concat([df_new_2, df_new], sort=False).drop_duplicates(subset=['time']))
#full_df = full_df.merge()
#print(full_df.tail(n=5))
print(full_df)
#full_df_2 = pd.concat([df_new_2, full_df], sort=False).drop_duplicates(subset=['time'])
#print(full_df_2)

#df = getData.update_list()
# print(df.keys())
# print(file)

# file_counter = getData.get_file_list()
# if len(file_counter) == 0:
#     df = getData.update_list()
# else:
#     df = getData.update_list()
#
# print(df.keys())
# print(df.tail(n=10))
# print(df.keys())



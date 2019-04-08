import krakenex
from pykrakenapi import KrakenAPI
import pandas as pd
from datetime import datetime
import os
import os.path
import shutil

DIR_DATA = "~/programming/Python/CryptoPrediction/"
DIR_CURRENT = "./cryptoData/currentData/"
DIR_ARCHIVE = "./cryptoData/archive/"
FULL_FILE = "BCHUSD_Full.csv"


def fetch_data():
    api = krakenex.API()
    k = KrakenAPI(api)
    ohlc, last = k.get_ohlc_data("BCHUSD")
    #print(ohlc)
    return ohlc, last

# def update_full_list(full_df):
#     if os._exists(os.path.join(DIR_CURRENT, FULL_FILE)):
#         full_df =

def save_to_file():
    # Fetch the data from Kraken
    ohlc, time = fetch_data()
    # Converts fetched data to DataFrame, else it will be as Tuple
    df = pd.DataFrame(ohlc, columns=['time', 'open', 'high', 'low', 'close', 'volume'])
    # Converts from UNIX time to formatted
    time = datetime.fromtimestamp(time).strftime('%Y-%m-%d_%H:%M:%S')
    # Sets the correct file name with currency and fetched/converted timestamp
    file_name = f"BCHUSD_{time}.csv"
    # Creates the CSV file with data
    df.to_csv(os.path.join(DIR_CURRENT, file_name), sep=',', index='dtime')
    return df, file_name


def get_file_list():
    names = []

    for root, dirs, files in os.walk(DIR_CURRENT):
        for filename in files:
            names.append(filename)

    names.sort()
    return names


# def GetFileIntoDF(filename):
#     path = DIR_CURRENT + filename
#     df = pd.read_csv(path, skiprows=[1], header=None)
#     return df


#def update_list():
    # files = get_file_list()
    #
    # #if os.exists(os.path.join(DIR_CURRENT, FULL_FILE)):
    # #    continue
    # #else:
    # #    full_file = pd.DataFrame(fetch_data(), columns=[''])
    # #    full_file.to_csv(os.path.join(DIR_CURRENT, FULL_FILE), sep=',', header=False)
    # # if len(files) <= 1:
    # #     print("Folder of current files are has only Full." + "\n" + "Importing new Delta")
    # #     # Fetch the data into files
    # #     df_temp, new_file_name = save_to_file()
    # #     # Add file name to the list
    # #     # files.append(new_file_name)
    # #     return df_temp
    # # else:
    # #     # takes the last file from array
    # #     #last_file = files[-1]
    # #     # Read the last file from currentData folder
    # #     #df = pd.read_csv(os.path.join(DIR_CURRENT, last_file), sep=',')
    # #     #df = pd.DataFrame(df)
    # #     # Fetch new data
    # #     df_temp, new_file_name = save_to_file()
    # #     # Adds new file name to the array and reselect the latest file
    # #     files.append(new_file_name)
    # #     last_file = files[-1]
    # #
    # #     # for f in files:
    # #     #    df = [GetFileIntoDF(file) for file in files]
    # #     #    unique_df = pd.merge(df, df_temp, on=['dtime'])
    # #     # new_df = pd.concat([df, df_temp], sort=False)
    # #     # unique_df = pd.merge(df, df_temp, left_on='time', right_on='time', how='left')
    # #     # unique_df = new_df.drop_duplicates()
    # #     # csv_files = []
    # #
    # #     # Merge the old and new files into one.
    # #     unique_df = pd.concat([df, df_temp]).drop_duplicates().reset_index(drop=True)
    # #     #unique_df = pd.concat([df, df_temp], sort=True)
    # #     #print(df.keys())
    # #     #print(df_temp.keys())
    # #     #unique_df = pd.merge(df, df_temp, on='time')
    # #     #unique_df = unique_df.drop_duplicates()
    # #     # unique_df.to_csv(os.path.join(DIR_CURRENT, new_file_name), sep=' ')
    # #     # unique_df.sort_values(by='time',ascending=False, inplace=True)
    # #
    # #     #unique_df.drop_duplicates(inplace=True, keep='first')
    # #     #unique_df.to_csv(os.path.join(DIR_CURRENT, "BCHUSD_fullData.csv"), sep=' ')
    # #
    # #     # Moves files to archive folder
    # #     for f in files:
    # #         if f != last_file:
    # #             move_archive(f)
    # #     #return df
    # #     return unique_df
    # if len(files) <= 1:
    #     print("Current folder has only Full file" + "/n" + "Importing new delta")
    #     df_delta, file_name = save_to_file()
    #
    #     df_full = pd.DataFrame(pd.read_csv(os.path.join(DIR_CURRENT, FULL_FILE),
    #                                    sep=',', header=False, index_col='dtime'))
    #     #print(df_delta.keys())
    #     print(df_full.keys())
    #
    #     df_full = df_full.merge(df_delta, on=['time'])
    #     df_full = df_full.drop_duplicates()
    #     return df_full
    # else:
    #     print('Breaking else...')



def move_archive(filename):
    shutil.move(os.path.join(DIR_CURRENT, filename), os.path.join(DIR_ARCHIVE, filename))

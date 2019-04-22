import krakenex
from pykrakenapi import KrakenAPI
import pandas as pd
from datetime import datetime
import os
import os.path
import shutil
from pathlib import Path, PureWindowsPath

import requests

# the path format set as Windows. Using pathlib converting the path to current environment.
#DIR_DATA = PureWindowsPath("CryptoPrediction\\cryptoData\\")
DIR_CURRENT = Path(PureWindowsPath(".\\cryptoData\\currentData\\"))
DIR_ARCHIVE = Path(PureWindowsPath(".\\cryptoData\\archive\\"))

print(DIR_CURRENT)
print(DIR_ARCHIVE)



# DIR_DATA = "~/programming/Python/CryptoPrediction/"
# DIR_CURRENT = "./cryptoData/currentData/"
# DIR_ARCHIVE = "./cryptoData/archive/"
FULL_FILE = "BCHUSD_Full.csv"


def fetch_data():
    api = krakenex.API()
    k = KrakenAPI(api)
    ohlc, last = k.get_ohlc_data("BCHUSD")
    return ohlc, last


def save_to_file(df, time):
    if time != 0:
        # Converts from UNIX time to formatted
        time = datetime.fromtimestamp(time).strftime('%Y-%m-%d_%H:%M:%S')
        # Sets the correct file name with currency and fetched/converted timestamp
        file_name = f"BCHUSD_{time}.csv"
        full_path = os.path.join(DIR_CURRENT, file_name)
        print(full_path)
        # Creates the CSV file with data
        #df.to_csv(os.path.join(DIR_CURRENT, file_name), sep=',', index='dtime')
        df.to_csv(full_path, mode='w', sep=',', index_label='dtime')
    else:
        #df.to_csv(os.path.join(DIR_CURRENT, FULL_FILE), sep=',', index='dtime')
        df.to_csv(os.path.join(DIR_CURRENT, FULL_FILE), sep=',', index=False)
    return df


def get_file_list():
    names = []
    for root, dirs, files in os.walk(DIR_CURRENT):
        for filename in files:
            names.append(filename)

    names.sort()
    return names


def updated_full():
    df_new, time = fetch_data()
    #print(df_new.tail(2))

    if os.path.isfile(FULL_FILE):
        df_full = save_to_file(df_new, 0)
        #print('Doing the IF NOT')
    else:
        #print('Doing the IF')
        save_to_file(df_new, time)
        #df_full = pd.read_csv(os.path.join(DIR_CURRENT, FULL_FILE), index_col='dtime')
        df_full = pd.read_csv(os.path.join(DIR_CURRENT, FULL_FILE), index_col='dtime')
        df_full = pd.concat([df_new, df_full], sort=False).drop_duplicates(subset=['time'], inplace=False)
        save_to_file(df_full, 0)

        files_count = get_file_list()
        for f in files_count:
            if f != FULL_FILE:
                #move_archive(f)
                pass
            else:
                pass
    df_full.set_index("time", inplace=True)
    print(df_full.keys())
    return df_full


def move_archive(filename):
    shutil.move(os.path.join(DIR_CURRENT, filename), os.path.join(DIR_ARCHIVE, filename))
    #shutil.move(DIR_CURRENT / filename, DIR_ARCHIVE / filename)

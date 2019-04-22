import os
#import pandas as pd
import numpy as np
import random
from collections import deque
from cryptoData import getData
from sklearn import preprocessing
from datetime import datetime
from pathlib import Path, PureWindowsPath

#DIR_PATH = os.path.dirname(os.path.abspath(__file__))
#DIR_DATA = "~/programming/Python/CryptoPrediction/"
DIR_CURRENT = Path(PureWindowsPath("cryptoData\\currentData\\"))
DIR_ARCHIVE = Path(PureWindowsPath("cryptoData\\archive\\"))

SEQ_LEN = 60


def modify_df(df):
    # new_df = df.drop(columns="time" "open" "high")
    new_df = df[['close', 'volume']]
    return new_df


def preprocess_df(df):
    for col in df.columns:
        df[col] = df[col].pct_change()
        df.dropna(inplace=True)
        df[col] = preprocessing.scale(df[col].values)

    df.dropna(inplace=True)

    sequential_data = []
    prev_days = deque(maxlen=SEQ_LEN)

    for i in df.values:
        prev_days.append([n for n in i[:-1]])
        if len(prev_days) == SEQ_LEN:
            sequential_data.append([np.array(prev_days), i[-1]])

    random.shuffle(sequential_data)

    buys = []
    sells = []

    for seq, target in sequential_data:
        if target == 0:
            sells.append([seq, target])
        elif target == 1:
            buys.append([seq, target])

    random.shuffle(buys)
    random.shuffle(sells)

    lower = min(len(buys), len(sells))

    buys = buys[:lower]
    sells = sells[:lower]

    sequential_data = buys + sells
    random.shuffle(sequential_data)

    X = []
    y = []

    for seq, target in sequential_data:
        X.append(seq)
        y.append(target)

    return np.array(X), y

#---------------------------


main_df = getData.updated_full()
print(main_df.tail(5))
#df = getData.updated_full()

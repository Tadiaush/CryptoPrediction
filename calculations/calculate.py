import pandas as pd
import numpy as np
import random
from collections import deque
from sklearn import preprocessing

from cryptoData import getDataYearly

SEQ_LEN = 60


def modify_data(full_df):
    main_df = pd.DataFrame()
    df = full_df[['Close', 'Volume (BTC)']]

    if len(main_df) == 0:
        main_df = df
    else:
        main_df = main_df.join(df)

    main_df.fillna(method='ffill', inplace=True)
    main_df.dropna(inplace=True)
    #print(main_df.head(5))

    return main_df


def classify(current, future):
    # Checking the future price with the current one. If future bigger than current, then it's a buy. Otherwise - sell
    if float(future) > float(current):
        return 1
    else:
        return 0


def preprocess_df(df):
    df = df.drop("future", 1)

    for col in df.columns:
        if col != 'target':
            df[col] = df[col].pct_change()
            df[col].replace([np.inf, -np.inf], np.nan, inplace=True)
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

    # list to store the buy sequences and targets
    buys = []
    # list to store the sells sequences and targets
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


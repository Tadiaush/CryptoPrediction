import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, CuDNNLSTM, BatchNormalization, Layer
from tensorflow.keras.callbacks import TensorBoard
from tensorflow.keras.callbacks import ModelCheckpoint

import time
from pathlib import Path, PureWindowsPath
from cryptoData import getData, getDataYearly
from calculations import calculate

# DIR_PATH = os.path.dirname(os.path.abspath(__file__))
# DIR_DATA = "~/programming/Python/CryptoPrediction/"
DIR_CURRENT = Path(PureWindowsPath("cryptoData\\currentData\\"))
DIR_ARCHIVE = Path(PureWindowsPath("cryptoData\\archive\\"))

# SEQ_LEN = 60
FUTURE_PERIOD_PREDICT = 3
EPOCHS = 6
BATCH_SIZE = 64
NAME = f"Output_{int(time.time())}"
start_time, end_time = '2018-03-01', '2019-03-01'

# ---------------------------
df = getDataYearly.import_data()
main_df = getDataYearly.clear_data(df)

main_df.fillna(method='ffill', inplace=True)
main_df.dropna(inplace=True)

main_df['future'] = main_df['Close'].shift(-FUTURE_PERIOD_PREDICT)
main_df['target'] = list(map(calculate.classify, main_df['Close'], main_df['future']))

main_df.dropna(inplace=True)
# print(main_df)

times = sorted(main_df.index.values)
last_5pct = sorted(main_df.index.values)[-int(0.1 * len(times))]

# making the validation data. Last 5% from main_df. And now the main_df has 95% to not duplicate the date.
validation_main_df = main_df[(main_df.index >= last_5pct)]
main_df = main_df[(main_df.index < last_5pct)]

# print(validation_main_df)
# print(main_df)

train_x, train_y = calculate.preprocess_df(main_df)
validation_x, validation_y = calculate.preprocess_df(validation_main_df)

print(f'train data: {len(train_x)} validation: {len(validation_x)}')
print(f'Dont buys: {train_y.count(0)}, buys: {train_y.count(1)}')
print(f'Validation dont buys: {validation_y.count(0)}, buys: {validation_y.count(1)}')


model = Sequential()
model.add(CuDNNLSTM(128, input_shape=(train_x.shape[1:]), return_sequences=True))
model.add(Dropout(0.2))
model.add(BatchNormalization())

model.add(CuDNNLSTM(128, return_sequences=True))
model.add(Dropout(0.1))
model.add(BatchNormalization())

model.add(CuDNNLSTM(128))
model.add(Dropout(0.2))
model.add(BatchNormalization())

model.add(Dense(32, activation='relu'))
model.add(Dropout(0.2))

model.add(Dense(2, activation='softmax'))

#print(model.summary())

opt = tf.keras.optimizers.Adam(lr=0.001, decay=1e-6)

# Compile model
model.compile(
    loss='sparse_categorical_crossentropy',
    optimizer=opt,
    metrics=['accuracy']
)

tensorboard = TensorBoard(log_dir="logs/{}".format(NAME))

filepath = "RNN_Final-{epoch:02d}-{val_acc:.3f}"  # unique file name that will include the epoch and the validation acc for that epoch
checkpoint = ModelCheckpoint("models/{}.model".format(filepath, monitor='val_acc', verbose=1, save_best_only=True,
                                                      mode='max'))  # saves only the best ones

# Train model
history = model.fit(
    train_x, train_y,
    batch_size=BATCH_SIZE,
    epochs=EPOCHS,
    validation_data=(validation_x, validation_y),
    callbacks=[tensorboard, checkpoint])

# Score model
score = model.evaluate(validation_x, validation_y, verbose=0)
print('Test loss:', score[0])
print('Test accuracy:', score[1])
# Save model
#model.save("models/{}".format(NAME))

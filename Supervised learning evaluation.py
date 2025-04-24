import numpy as np
from keras.losses import categorical_crossentropy, binary_crossentropy
from keras.utils import to_categorical
from keras.layers import *
from keras.models import Sequential
from keras.callbacks import EarlyStopping

# W&B Imports
import wandb
from wandb.keras import WandbCallback


# Load data
path = 'C:\\Users\\Rigos\\Documents\\GitHub\\ChessEngine\\datasets\\dataset4\\'

for i in range(1, 8):
    globals()['board{}'.format(i)] = np.load(path + "dataset4X{0}.txt".format(i), allow_pickle=True)
    globals()['eval{}'.format(i)] = np.load(path + "dataset4y{0}.txt".format(i), allow_pickle=True)



board1 = np.load(path + "dataset4X1.txt", allow_pickle=True)
board2 = np.load(path + "dataset4X2.txt", allow_pickle=True)
board3 = np.load(path + "dataset4X3.txt", allow_pickle=True)
board4 = np.load(path + "dataset4X4.txt", allow_pickle=True)
board5 = np.load(path + "dataset4X5.txt", allow_pickle=True)
board6 = np.load(path + "dataset4X6.txt", allow_pickle=True)
board7 = np.load(path + "dataset4X7.txt", allow_pickle=True)
eval1 = np.load(path + "dataset4y1.txt", allow_pickle=True)
eval2 = np.load(path + "dataset4y2.txt", allow_pickle=True)
eval3 = np.load(path + "dataset4y3.txt", allow_pickle=True)
eval4 = np.load(path + "dataset4y4.txt", allow_pickle=True)
eval5 = np.load(path + "dataset4y5.txt", allow_pickle=True)
eval6 = np.load(path + "dataset4y6.txt", allow_pickle=True)
eval7 = np.load(path + "dataset4y7.txt", allow_pickle=True)

X_train = np.concatenate((board1, board2, board3, board4, board5, board6, board7))
y_train = np.concatenate((eval1, eval2, eval3, eval4, eval5, eval6, eval7))

# convert to list
y_train = np.ndarray.tolist(y_train)
normalised_y_train = []
normalised_X_train = []

for index, y in enumerate(y_train):
    if y >= 0:
        normalised = 0
        normalised_y_train.append(normalised)

    elif y < 0:
        normalised = 1
        normalised_y_train.append(normalised)


# # scale the evals to values between 0 and 1
# for y in y_train:
#     normalised = (y+10)/20
#     normalised_y_train.append(normalised)

y_train = np.asarray(normalised_y_train)
normalised_y_train.clear()

y_train = to_categorical(y_train)
print(X_train.shape)
print(y_train.shape)
print(y_train[0:10])

# s = np.arange(X_train.shape[0])
# np.random.shuffle(s)
# X_train = X_train[s]
# y_train = y_train[s]
# X_train[X_train < 0] = 1

wandb.init(project="chess-cnn")

"""""""""""""""""""""
Network architecture
"""""""""""""""""""""

model = Sequential()
# Convolutional layer
model.add(Conv2D(20, kernel_size=(5, 5), padding='same',input_shape=(8, 8, 12)))
model.add(Activation('relu'))
model.add(Conv2D(50, (3, 3), padding='same'))
model.add(Activation('relu'))
# Dropout to avoid overfitting
model.add(Dropout(0.3))
# Convert to suitable form for the dense layer
model.add(Flatten())
model.add(Dense(220))
model.add(Dense(2, activation="relu"))
model.compile(loss="binary_crossentropy", optimizer='adam', metrics=["accuracy"])

"""""""""""""""
Model training
"""""""""""""""

# start the training
model.fit(X_train, y_train, epochs=3, batch_size=64, verbose=1, validation_split=0.1,
                   callbacks=[WandbCallback()])#, EarlyStopping(monitor='val_loss', patience=int(10))])

# save the model in a file
model.save('example_model')


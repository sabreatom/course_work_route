from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.callbacks import EarlyStopping
from keras.callbacks import Callback

from numpy import genfromtxt
import numpy as np
import sys
import matplotlib.pyplot as plt

# fix random seed for reproducibility
np.random.seed(7)

#Import aggregated data, day numbering need to start from zero:
gps_data = genfromtxt('aggregated_data.csv', delimiter=',', skip_header=1)

#Create dataset dataset:
x=[[]] #coordinates per day
y=[] #day type
first_time = True
for row in gps_data:
    if (first_time): #first row
        if (row[0] == 0):
            day_num = row[0]
            sequence_num = 0
            x[sequence_num].append([round(row[1], 4), round(row[2], 4)])
            y.append(row[3])
            first_time = False
        else:
            print "[ERROR] Day numbering in CSV file need to start from 0."
            sys.exit()
    else:
        if (day_num == row[0]):
            x[sequence_num].append([round(row[1], 4), round(row[2], 4)])
        else:
            day_num = row[0]
            sequence_num = sequence_num + 1
            x.append([])
            x[sequence_num].append([round(row[1], 4), round(row[2], 4)])
            y.append(row[3])

#Find out max number of coordinates per day:
max_value = 0
for day in x:
    if (len(day) > max_value):
        max_value = len(day)

#if number of coordinat per day is less then max then append zero coordinats:
for day in x:
    if (len(day) > max_value):
        day = day[0:max_value]
    else:
        for j in range((max_value - len(day))):
            day.append([0.0,0.0])

x = np.array(x) #convert to numpy array
y = np.array(y) #convert to numpy array

x = np.reshape(x, (x.shape[0], 2, x.shape[1]))

#Callbacks:
class My_Callback(Callback):
    def on_epoch_end(self, epoch, logs={}):
        if logs.get('val_acc') > 0.8:
            self.model.stop_training = True

callbacks = [My_Callback()]

#callbacks = [ EarlyStopping(monitor='val_acc', min_delta=0, patience=50, verbose=0, mode='auto') ]

#Create sequential neural network model three layers:
model1 = Sequential()
model1.add(LSTM(50, input_shape=(2,max_value)))
model1.add(Dense(1, activation='sigmoid'))
model1.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
history1 = model1.fit(x, y, validation_split=0.2, epochs=500, batch_size=32, verbose=0, callbacks=callbacks)

#Create sequential neural network model three layers:
model2 = Sequential()
model2.add(LSTM(50, input_shape=(2,max_value)))
model2.add(Dense(30, activation='relu'))
model2.add(Dense(1, activation='sigmoid'))
model2.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
history2 = model2.fit(x, y, validation_split=0.2, epochs=500, batch_size=32, verbose=0, callbacks=callbacks)

#Create sequential neural network model two layers and smaller number of elements:
model3 = Sequential()
model3.add(LSTM(30, input_shape=(2,max_value)))
model3.add(Dense(1, activation='sigmoid'))
model3.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
history3 = model3.fit(x, y, validation_split=0.2, epochs=500, batch_size=32, verbose=0, callbacks=callbacks)

#Create sequential neural network model three layers and smaller number of elements:
model4 = Sequential()
model4.add(LSTM(30, input_shape=(2,max_value)))
model4.add(Dense(5, activation='relu'))
model4.add(Dense(1, activation='sigmoid'))
model4.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
history4 = model4.fit(x, y, validation_split=0.2, epochs=500, batch_size=32, verbose=0, callbacks=callbacks)

#Plot results:
plt.subplot(2, 2, 1)  
plt.plot(history1.history['acc'], 'r', label = 'Accuracy')
plt.plot(history1.history['loss'], 'g', label = 'Loss')
plt.plot(history1.history['val_acc'], 'b', label = 'Validation accuracy')

plt.subplot(2, 2, 2)  
plt.plot(history2.history['acc'], 'r', label = 'Accuracy')
plt.plot(history2.history['loss'], 'g', label = 'Loss')
plt.plot(history2.history['val_acc'], 'b', label = 'Validation accuracy')

plt.subplot(2, 2, 3)  
plt.plot(history3.history['acc'], 'r', label = 'Accuracy')
plt.plot(history3.history['loss'], 'g', label = 'Loss')
plt.plot(history3.history['val_acc'], 'b', label = 'Validation accuracy')

plt.subplot(2, 2, 4)  
plt.plot(history4.history['acc'], 'r', label = 'Accuracy')
plt.plot(history4.history['loss'], 'g', label = 'Loss')
plt.plot(history4.history['val_acc'], 'b', label = 'Validation accuracy')

plt.show()

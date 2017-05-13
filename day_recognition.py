from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM

from numpy import genfromtxt
import numpy as np
import sys

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

#Create sequential neural network model:
model = Sequential()
model.add(LSTM(32, input_shape=(2,max_value)))
model.add(Dense(1, activation='sigmoid'))
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
model.fit(x, y, epochs=1000, batch_size=10, verbose=0)
print model.predict(x)


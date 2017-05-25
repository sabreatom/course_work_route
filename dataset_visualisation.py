from numpy import genfromtxt
import sys
import matplotlib.pyplot as plt

#Import aggregated data, day numbering need to start from zero:
gps_data = genfromtxt('aggregated_data.csv', delimiter=',', skip_header=1)

#Create dataset dataset:
x=[[[],[]]] #coordinates per day
y=[] #day type
first_time = True
for row in gps_data:
    if (first_time): #first row
        if (row[0] == 0):
            day_num = row[0]
            sequence_num = 0
            x[sequence_num][0].append(round(row[1], 4))
            x[sequence_num][1].append(round(row[2], 4))
            y.append(row[3])
            first_time = False
        else:
            print "[ERROR] Day numbering in CSV file need to start from 0."
            sys.exit()
    else:
        if (day_num == row[0]):
            x[sequence_num][0].append(round(row[1], 4))
            x[sequence_num][1].append(round(row[2], 4))
        else:
            day_num = row[0]
            sequence_num = sequence_num + 1
            x.append([[],[]])
            x[sequence_num][0].append(round(row[1], 4))
            x[sequence_num][1].append(round(row[2], 4))
            y.append(row[3])

#Working days:
plt.subplot(2, 1, 1)   
for day in range(len(y)):
    if (y[day] == 1):
        plt.plot(x[day][0], x[day][1], 'r*')

#Free days:
plt.subplot(2, 1, 2)
for day in range(len(y)):
    if (y[day] == 0):
        plt.plot(x[day][0], x[day][1], 'g*')

plt.show()

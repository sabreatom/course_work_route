from numpy import genfromtxt
import math
from datetime import datetime
import matplotlib.pyplot as plt
from datetime import date
import calendar
import csv

#Array of dates holidays in the dataset:
holidays = []

def TypeOfDay(timestamp):
    day_of_week = calendar.day_name[datetime.fromtimestamp(timestamp).weekday()]
    if ((day_of_week == 'Saturday') or (day_of_week == 'Sunday')):
        return 0
    else:
        return 1

#import data:
gps_data = genfromtxt('gps.csv', delimiter=',')

tmp = []

#Clean data:
for row in gps_data:
    if ((not math.isnan(row[1])) and (not math.isnan(row[2])) and (not math.isnan(row[3]))):
        tmp.append([row[1], round(row[2],4), round(row[3],4)])

#Agregate data by days:
dataset = [[]]
dataset_day_type = []
day_num = 0
date = datetime.fromtimestamp(tmp[0][0]).day
dataset_day_type = [TypeOfDay(tmp[0][0])]
for row in tmp:
    if (datetime.fromtimestamp(row[0]).day == date):
        dataset[day_num].append([row[1], row[2]])
    else:
        date = datetime.fromtimestamp(row[0]).day
        day_num = day_num + 1
        dataset.append([])
        dataset[day_num].append([row[1], row[2]])
        dataset_day_type.append(TypeOfDay(row[0]))

print dataset[0]
print "Number of days in dataset: " + str(len(dataset))

#Write aggregated data to CSV file:
with open('aggregated_data.csv', 'wb') as csvfile:
    coorwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    day_counter = 0
    coorwriter.writerow(['Day number', 'Longitude', 'Latitude', 'Type of day'])
    for row in dataset:
        for coor in row:
            coorwriter.writerow([day_counter, coor[0], coor[1], dataset_day_type[day_counter]])

        day_counter = day_counter + 1

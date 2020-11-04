import csv
from datetime import datetime
from datetime import timedelta
import os


def convertDate(date):
    time = datetime.strptime(date, '%Y%m%d%H%M%S')
    return time
def getDay(date):
    return date[0:7]    
first = True
lastDay = getDay('20140317055456')
beginTime = convertDate('20140317055456')
print(lastDay)
for year in range(2014, 2020):
    filename = "en_ex_"
    filename += str(year)
    filename += "03.csv"
    with open("./sortedTestData/"+filename, mode='r') as csv_tmp:
        csv_reader = csv.DictReader(csv_tmp,fieldnames=['cardno','payno','datetime','line','staname','inout','cardsort','datetimein','linein','stain'])
        for row in csv_reader:
            now = getDay(row['datetime'])
            if now < lastDay :
                print("error")
            lastDay = now
        csv_tmp.close()
        
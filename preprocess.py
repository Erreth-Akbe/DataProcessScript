import csv
from datetime import datetime
from datetime import timedelta
import os
from functools import cmp_to_key
dataList = []

for year in range(2014, 2020):
    filename = "en_ex_"
    filename += str(year)
    filename += "03.csv"
    with open("./data/"+filename, mode='r',newline='') as csv_tmp:
        csv_reader = csv.reader(csv_tmp)
        for row in csv_reader:
            dataList.append(row)
        csv_tmp.close()
    print("---------load finish-------------")
    for data in dataList:
        if data[2] == data[7]:
            data[8] = ''
            data[9] = ''
            print(data)
    pathName4 = "./processedData/"
    if os.path.isdir(pathName4) == False:
        os.mkdir(pathName4)
    with open(pathName4+filename, mode='w',newline='') as csv_to_write:
        csv_writter = csv.writer(csv_to_write, delimiter=',')
        for row in dataList:
            csv_writter.writerow(row)
        csv_to_write.close()
    dataList = []
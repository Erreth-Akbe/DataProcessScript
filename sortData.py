import csv
from datetime import datetime
from datetime import timedelta
import os
from functools import cmp_to_key
dataList = []
def convertDate(date):
    time = datetime.strptime(date, '%Y%m%d%H%M%S')
    return time
def cmpList(a, b):
    at = a[2]
    bt = b[2]
    montha = int(at[4:6])
    daya = int(at[6:8])
    houra = int(at[8:10])
    mina = int(at[10:12])
    seconda = int(at[12:14])
    monthb = int(bt[4:6])
    dayb = int(bt[6:8])
    hourb = int(bt[8:10])
    minb = int(bt[10:12])
    secondb = int(bt[12:14])
    #print(at)
    #print(bt)
    if montha > monthb:
        return 1
    elif montha < monthb:
        return -1
    else:
        if daya > dayb:
            return 1
        elif daya < dayb:
            return -1
        else:
            if houra > hourb:
                return 1
            elif houra < hourb:
                return -1
            else:
                if mina > minb:
                    return 1
                elif mina < minb:
                    return -1
                else:
                    if seconda > secondb:
                        return 1
                    elif seconda < secondb:
                        return -1
                    else:
                        return 0
    

for year in range(2014, 2020):
    filename = "en_ex_"
    filename += str(year)
    filename += "03.csv"
    with open("./processedData/"+filename, mode='r',newline='') as csv_tmp:
        csv_reader = csv.reader(csv_tmp)
        for row in csv_reader:
            dataList.append(row)
        csv_tmp.close()
    print("---------load finish-------------")
    dataList.sort(key=cmp_to_key(cmpList))
    pathName4 = "./sortedData/"
    if os.path.isdir(pathName4) == False:
        os.mkdir(pathName4)
    with open(pathName4+filename, mode='w',newline='') as csv_to_write:
        csv_writter = csv.writer(csv_to_write, delimiter=',')
        for row in dataList:
            csv_writter.writerow(row)
        csv_to_write.close()
    dataList = []
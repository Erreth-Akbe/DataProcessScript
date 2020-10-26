import csv
from datetime import datetime
from datetime import timedelta
import os
#总字典
allDict = dict()
#四个字典，分别依次对应通勤人员，老人，残疾人，中小学生的普通出行数据
fourNomalDict = []
#四个字典 同上记录四种人员的出站入站数据
fourAdvanceDict = []
#四个list，用于统计四种人群的站点数据
fourStationDict = []
fourStationList = []
#一个list，其中有两个元素，分别对应：0->工作日，1->周末，用于统计站点进出数据
for i in range(0, 4):
    stationList = []
    stationDict = []
    for j in range(0, 2):
        stationDict.append(dict())
    for j in range(0, 2):
        stationList.append([])
    fourStationList.append(stationList)
    fourStationDict.append(stationDict)

ONEHOUREND = datetime.strptime("2020010101000", '%Y%m%d%H%M%S')
ONEHOURBEGIN = datetime.strptime("2020010100000", '%Y%m%d%H%M%S')
ONEHOURTIME = ONEHOUREND-ONEHOURBEGIN
print(ONEHOURTIME)

for i in range(0, 4):
    fourNomalDict.append(dict())
    fourAdvanceDict.append(dict())

def convertDate(date):
    time = datetime.strptime(date, '%Y%m%d%H%M%S')
    return time

def getHourlyChime(dt, step=0):
    """
    计算整小时的时间
    :param step: 往前或往后跳跃取整值，默认为0，即当前所在的时间，正数为往后，负数往前。
                例如：
                step = 0 时 2019-04-11 17:38:21.869993 取整秒后为 2019-04-11 17:38:21
                step = 1 时 2019-04-11 17:38:21.869993 取整秒后为 2019-04-11 17:38:22
                step = -1 时 2019-04-11 17:38:21.869993 取整秒后为 2019-04-11 17:38:20
    :return: 整理后的时间戳
    """
    # 整小时
    td = timedelta(days=0, seconds=dt.second, microseconds=dt.microsecond, milliseconds=0, minutes=dt.minute, hours=-step, weeks=0)
    new_dt = dt - td
    return new_dt

def initDict(fourStationDict):
    for people in fourStationDict:
        for week in people:
            for station in week:
                for inout in station:
                    inout = 0

def getPeopleType(cardsort):
    if cardsort == 0:
        return 0
    if cardsort == '1106':
        return 1
    elif cardsort == '1104':
        return 2
    elif cardsort == '1112':
        return 3
    return -1

def isWorkTime(datetime,stain, staout):
    hour = int(datetime[8:10])
    minute = int(datetime[10:12])
    second = int(datetime[12:14])
    timeType = 2
    if hour >=5 and hour <= 10:
        timeType = 0
    if hour >17 and hour <= 23:
        timeType = 1
    if hour == 14 and minute >= 30:
        timeType = 1
    return timeType
def getPeopleName(type):
    if type == 1:
        return "old"
    elif type == 2:
        return "disable"
    elif type == 3:
        return "student"

def getIsChangeType(table):  
    if table == []:
        return 0
    stain = table[0][5]
    staout = table[0][2]
    inChange = False
    outChange = False
    for row in table:
        if stain != row[5]:
            inChange = True
        if staout != row[2]:
            outChange = True
    if inChange == False and outChange == False:
        return 0
    elif inChange and outChange == False:
        return 1
    elif inChange == False and outChange:
        return 2
    elif inChange and outChange:
        return 3

def getIsChangeName(table):
    type = getIsChangeType(table)
    if type == 0:
        return "notChange"
    elif type == 1:
        return "inChange"
    elif type == 2:
        return "outChange"
    elif type == 3:
        return "allChange"

def getWeekName(isChangetType):
    if isChangetType == 0:
        return 'workday'
    elif isChangetType == 1:
        return 'weekend'

def getWeekType(now):
    week = now.weekday()
    type = 0
    if week >= 0 and week <= 4:
        type =  0
    elif weel > 4 and week <= 6:
        type = 1
    return type

def getNomalDict(type):
    return fourNomalDict[type]

def getAdvanceDict(type):
    return fourAdvanceDict[type]

def getStationDict(peopleType, now):
    week = getWeekType(now)
    return fourStationDict[peopleType][week]

def getStationList(peopleType, weekType):
    return fourStationList[peopleType][weekType]


def handleNull(id, dic):
    if id not in dic:
        dic[id] = []

def handleStationNull(id, dic):
    if id not in dic:
        dic[id] = []
        dic[id].append(0)
        dic[id].append(0)

def processHourlyStation(fourStationDict, id, now, inout, peopleType):
    weekType = getWeekType(now)
    dic = fourStationDict[peopleType][weekType]
    inoutType = int(inout)%2
    dic[id][inoutType] += 1


def inputNomalData(tables, cardno, datetime, line, staname, inout, cardsort):
    tmp = []
    tmp.append(cardno)
    tmp.append(datetime)
    tmp.append(line)
    tmp.append(staname)
    tmp.append(inout)
    tmp.append(cardsort)
    tables.append(tmp)

def inputAdvanceData(tables, cardno, datetime, staname, line, datetimein, stain, linein, gap, cardsort):
    tmp = []
    tmp.append(cardno)
    tmp.append(datetime)
    tmp.append(staname)
    tmp.append(line)
    tmp.append(datetimein)
    tmp.append(stain)
    tmp.append(linein)
    tmp.append(gap)
    tmp.append(cardsort)
    #print(tmp)
    tables.append(tmp)

def inputStationData(fourStationDict, fourStationList, beginTime, now):
    
    for peopleType in range(0, 4):
        for weekType in range(0, 2):
            tables = getStationList(peopleType, weekType)
            dic = getStationDict(peopleType, now)
            tmp = []
            tmp.append(beginTime)
            tmp.append(now)
            for station in dic:
                tmp.append(station[0])
                tmp.append(station[1])
            #print(tmp)
            tables.append(tmp)

beginTime = convertDate('20140317055456')
first = True
for year in range(2014, 2020):
    filename = ""
    filename += "en_ex_"
    filename += str(year)
    filename += "03.csv"
    with open("./testdata/"+filename, mode='r') as csv_tmp:
        csv_reader = csv.DictReader(csv_tmp,fieldnames=['cardno','payno','datetime','line','staname','inout','cardsort','datetimein','linein','stain'])
        
        for row in csv_reader:
            if first:
                first = False
                beginTime = getHourlyChime(convertDate(row['datetime']))
                initDict(fourStationDict)
            now =  getHourlyChime(convertDate(row['datetime']))
            id = row['cardno']
            type = getPeopleType(row['cardsort'])
            stationId = row['staname']
            handleNull(id, allDict)
            handleStationNull(stationId, getStationDict(0, now))
            if now-beginTime >= ONEHOURTIME:
                inputStationData(fourStationDict, fourStationList, beginTime, now)
                beginTime = now
                initDict(fourStationDict)
            processHourlyStation(fourStationDict, stationId, now, row['inout'], 0)
            # process three types
            if type != -1 :
                handleNull(id, getNomalDict(type))
                handleNull(id, getAdvanceDict(type))
                handleStationNull(stationId, getStationDict(type, now))
                processHourlyStation(fourStationDict, stationId, now, row['inout'], type)
                inputNomalData(getNomalDict(type)[id], row['cardno'], row['datetime'], row['line'], row['staname'], row['inout'], row['cardsort'])
                if row['stain'] != '':
                    inputAdvanceData(getAdvanceDict(type)[id], row['cardno'],  row['datetime'], row['staname'], row['line'], 
                                        row['datetimein'], row['stain'], row['linein'], int(row['datetime'])-int(row['datetimein']), row['cardsort'])
            
        csv_tmp.close()
        for j in range(1, 4):
            filename = str(year)+".csv"
            pathName4 = "./data/out/"+getPeopleName(j)+"/4_chain/"
            if os.path.isdir(pathName4) == False:
                os.mkdir(pathName4)
            with open(pathName4+filename, mode='w') as csv_to_write:
                csv_writter = csv.writer(csv_to_write, delimiter=',')
                firstRow = [ 'cardno', 'datetime', 'staname', 'line', 'datetimein', 'stain', 'linein', 'gap', 'cardsort']
                csv_writter.writerow(firstRow)
                for key in getAdvanceDict(i):
                    tables = getAdvanceDict(i)[key]
                    for row in tables:
                        csv_writter.writerow(row)
                csv_to_write.close()
            pathName5 = "./data/out/"+getPeopleName(j)+"/5_isChange/"
            if os.path.isdir(pathName5) == False:
                os.mkdir(pathName5)
            for key in getAdvanceDict(j):
                tables = getAdvanceDict(j)[key]
                filename = pathName5+getIsChangeName(tables)+str(year)+".csv";
                with open(filename, mode='w') as csv_to_write:
                    csv_writter = csv.writer(csv_to_write, delimiter=',')
                    for row in tables:
                        csv_writter.writerow(row)
                    csv_to_write.close()
            for key in getAdvanceDict(j):
                getAdvanceDict(j)[key] = []

print("----------load finish---------")

for i in range(1, 4):
    filename = '(1)原始卡号数据.csv'
    with open("./data/out/"+getPeopleName(i)+"/"+filename, mode='w') as csv_tmp:
        csv_writter = csv.writer(csv_tmp, delimiter=',')
        firstRow = ['cardno', 'datetime', 'line', 'staname', 'inout', 'cardsort']
        csv_writter.writerow(firstRow)
        for key in getNomalDict(i):
            tables = getNomalDict(i)[key]
            for row in tables:
                csv_writter.writerow(row)
        



for i in range(1, 4):
    for j in range(0, 2):
        filename = '.csv'
#        print(getPeopleName(i))
#        print(getWeekName(j))
        with open("./data/out/"+getPeopleName(i)+"/"+getWeekName(j)+"/(3)"+filename, mode='w') as csv_tmp:
            csv_writter = csv.writer(csv_tmp, delimiter=',')
            firstRow = [ 'beginTime', 'endTime']
            for key in fourStationDict[i][j]:
                firstRow.append(key+'in')
                firstRow.append(key+'out')
            csv_writter.writerow(firstRow)
            for row in getStationList(i, j):
                csv_writter.writerow(row)
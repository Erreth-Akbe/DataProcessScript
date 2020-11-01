import csv
from datetime import datetime
from datetime import timedelta

timesInOneWeek = dict()
isWorkMoning = dict()
isWorkToday = dict()
# 这个地方是两个字典，里面hash的AB站点组合
isWorkMan = dict()
workPlace = dict()
homePlace = dict()
MAXSTATIONNUMBER = 1000
def handelTimesInOneWeekNull(id, timesInOneWeek):
    if id not in timesInOneWeek:
        timesInOneWeek[id] = 0
    return

def handelIsWorkTodayNull(id, isWorkToday):
    if id not in isWorkToday:
        isWorkToday[id] = False
    return

def handelisWorkManNull(id, isWorkMan):
    if  id not in isWorkMan:
        isWorkMan[id] = False
    return

def handelIsWorkMENull(id, isME):
    if id not in isME:
        isME[id] = dict()
    return

def initOneWeek(timesInOneWeek):
    for id in timesInOneWeek:
        timesInOneWeek[id] = 0
    return

def initOneDay(isWorkToday):
    for id in isWorkToday:
        isWorkToday[id] = False
    return

def initisWorkME(isworkM):
    isworkM.clear()
    return
        

def getDay(date):
    return date[0:7]

def getHashAB(stain, staout):
    return int(stain)*MAXSTATIONNUMBER+int(staout)
def getInverseHashAB(stain, staout):
    return int(stain)*MAXSTATIONNUMBER+int(staout)

def convertDate(date):
    time = datetime.strptime(date, '%Y%m%d%H%M%S')
    return time


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

def isWorkTime(date):
    hour = int(date[8:10])
    minute = int(date[10:12])
    second = int(date[12:14])
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
    elif week > 4 and week <= 6:
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

def isChangeDay(date, lastDay):
    if getDay(date) != getDay(lastDay):
        return True
    else:
        return False

def isChangeWeek(now, lastWeekType):
    nowWeekType = getWeekType(now)
    if (nowWeekType == 1):
        return False
    elif (nowWeekType == 0 and lastWeekType == 0):
        return False
    else:
        return True

def changeDay(isWorkToday, timesInOneWeek):
    for id in isWorkToday:
        if isWorkToday[id]:
            handelTimesInOneWeekNull(id, timesInOneWeek)
            timesInOneWeek[id] += 1
    initOneDay(isWorkToday)
    return

def changeWeek(timesInOneWeek, isWorkMan):
    for id in timesInOneWeek:
        if timesInOneWeek[id] >= 3:
            handelisWorkManNull(id, isWorkMan)
            isWorkMan[id] = True
    initOneWeek(timesInOneWeek)
    return



# preprocess find who is workman
# 打工人，打工魂，打工都是人上人
lastDay = getDay('20140317055456')
beginTime = convertDate('20140317055456')
lastWeekType = getWeekType(beginTime)
first = True
for year in range(2014, 2020):
    filename = "en_ex_"
    filename += str(year)
    filename += "03.csv"
    with open("./data/"+filename, mode='r') as csv_tmp:
        csv_reader = csv.DictReader(csv_tmp,fieldnames=['cardno','payno','datetime','line','staname','inout','cardsort','datetimein','linein','stain'])
        
        for row in csv_reader:
            if first:
                first = False
                beginTime = getHourlyChime(convertDate(row['datetime']))
                lastDay = getDay(row['datetime'])
                lastWeekType = getWeekType(beginTime)
            date = row['datetime']
            now = convertDate(date)
            nowType =  getWeekType(convertDate(row['datetime']))
            id = row['cardno']
            staname = row['staname']
            stain = row['stain']
            timeType = isWorkTime(date)
            if stain == '':
                continue
            if timeType == 0:
                handelIsWorkMENull(id, isWorkMoning)
                isWorkMoning[id][getHashAB(stain, staname)] = True
            elif timeType == 1:
                if id in isWorkMoning and getInverseHashAB(stain, staname) in isWorkMoning[id] and isWorkMoning[id][getInverseHashAB(stain, staname)]:
                    handelIsWorkTodayNull(id, isWorkToday)
                    isWorkToday[id] = True
                    workPlace[id] = stain
                    homePlace[id] = staname
            
            if isChangeDay(date, lastDay):
                changeDay(isWorkToday, timesInOneWeek)
            if isChangeWeek(now, lastWeekType):
                changeweek(timesInOneWeek, isWorkMan)
            lastDay = getDay(date)
            lastWeekType - getWeekType(now)
        csv_tmp.close()
  

print("----------preprocess Finished---------")
for id in isWorkMan:
    print(isWorkMan[id])
import csv
from datetime import datetime
from datetime import timedelta
import os
workManNormalDict = dict()
#四个字典 同上记录四种人员的出站入站数据
workManAdvanceDict = dict()
#四个list，用于统计四种人群的站点数据
workManStationDict = []
workManStationList = []
stationNameList = ['0146','0145','0144','0102','0103','0104','0143','0105','0106','0107','0108','0109','0110','0111','0112','0113','0114','0115','0116','0117','0118','0119','0120','0121','0122','0123','0124','0125','0126','0140','0141','0142','0224','0225','0226','0227','0228','0230','0231','0232','0233','0234','0235','0236','0237','0238','0239','0240','0241','0242','0243','0244','0245','0246','0247','0248','0249','0250','0251','0252','0253','0254','0255','0257','0258','0259','0260','0261','0331','0332','0333','0334','0335','0336','0337','0338','0340','0341','0342','0343','0344','0345','0346','0347','0348','0349','0350','0351','0352','0353','0354','0422','0423','0424','0425','0426','0427','0428','0429','0430','0431','0432','0433','0434','0435','0436','0437','0438','0439','0440','0441','0442','0443','0444','0445','0448','0449','0450','0451','0452','0453','0454','0455','0456','0457','0458','0631','0632','0633','0634','0635','0636','0637','0638','0639','0641','0642','0643','0644','0645','0646','0647','0648','0649','0650','0651','0652','0653','0654','0655','0656','0657','0731','0732','0733','0734','0735','0736','0737','0738','0739','0740','0741','0742','0743','0744','0745','0746','0747','0748','0749','0750','0751','0752','0753','0754','0755','0756','0831','0832','0833','0834','0835','0836','0837','0838','0839','0840','0841','0842','0854','0855','0856','1140','1141','1142','1143','1144','1145','1146','1147','1148','1149','1150','1151','1152','2131','2132','2133','2134','2135','2136','2137','2138','2139','2140','2141','2142','2143','2144','2145','2146']

#一个list，其中有两个元素，分别对应：0->工作日，1->周末，用于统计站点进出数据
for j in range(0, 2):
    workManStationDict.append(dict())
for j in range(0, 2):
    workManStationList.append([])

ONEHOUREND = datetime.strptime("2020010101000", '%Y%m%d%H%M%S')
HALFHOUREND = datetime.strptime("2020010100300", '%Y%m%d%H%M%S')
ONEHOURBEGIN = datetime.strptime("2020010100000", '%Y%m%d%H%M%S')
ONEHOURTIME = ONEHOUREND-ONEHOURBEGIN
HALFHOURTIME = HALFHOUREND-ONEHOURBEGIN
print(HALFHOURTIME)

timesInOneWeek = dict()
isWorkMorning = dict()
isWorkToday = dict()
# 这个地方是两个字典，里面hash的AB站点组合
isWorkMan = dict()
workManMoringData = dict()
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
        
def initDict(wrokManStationDict):
    for week in wrokManStationDict:
            for station in week:
                week[station][0] = 0
                week[station][1] = 0
def getDay(date):
    return date[0:8]

def getHashAB(stain, staout):
    #print("AB"+str(int(stain)*MAXSTATIONNUMBER+int(staout)))
    return int(stain)*MAXSTATIONNUMBER+int(staout)
def getInverseHashAB(stain, staout):
    #print("inversAB"+int(staout)*MAXSTATIONNUMBER+int(stain))
    return int(staout)*MAXSTATIONNUMBER+int(stain)

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
    elif hour >17 and hour <= 23:
        timeType = 1
    elif hour == 16 and minute >= 30:
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
def getHalfHourlyChime(dt, step=0):
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
    if dt-new_dt >= HALFHOURTIME:
        return new_dt+HALFHOURTIME
    else:
        return new_dt
def getIsChangeType(table):  
    if table == []:
        return 0
    homePlace = table[0][1]
    workPlace = table[0][2]
    inChange = False
    outChange = False
    for row in table:
        if homePlace != row[1]:
            inChange = True
        if workPlace != row[2]:
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
        return "homePlaceChange"
    elif type == 2:
        return "workPlaceChange"
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

def getStationDict(now):
    week = getWeekType(now)
    return workManStationDict[week]
def getStationList(weekType):
    return workManStationList[weekType]


def handleNull(id, dic):
    if id not in dic:
        dic[id] = []

def handleStationNull(id, dic):
    if id not in dic:
        dic[id] = []
        dic[id].append(0)
        dic[id].append(0)

def processHourlyStation(workManStationDict, id, now, inout):
    weekType = getWeekType(now)
    handleStationNull(id, getStationDict(now))
    dic = workManStationDict[weekType]
    inoutType = int(inout)%2
    dic[id][inoutType] += 1


def inputAdvanceData(tables, cardno, homePlace, workPlace,  cardsort, morningin, morningout, datein,  dateout):
    if homePlace == workPlace:
        return
    tmp = []
    tmp.append(cardno)
    tmp.append(homePlace)
    tmp.append(workPlace)
    tmp.append(cardsort)
    tmp.append(morningin)
    tmp.append(morningout)
    tmp.append(datein)
    tmp.append(dateout)
    tables.append(tmp)
    #print(tmp)


def inputMorningData(hashDiction, ABhash,cardno, datetime,staname, inout1, line, cardsort,datetimein, stain,inout2, linein):
    if ABhash not in hashDiction:
        tmp = []
        tmp.append(cardno)
        tmp.append(datetime)
        tmp.append(staname)
        tmp.append(inout1)
        tmp.append(line)
        tmp.append(cardsort)
        tmp.append(datetimein)
        tmp.append(stain)
        tmp.append(inout2)
        tmp.append(linein)
    #print(tmp)
        hashDiction[ABhash] = tmp


def inputNormalData(tables, cardno, datetime,staname, inout1, line, cardsort,datetimein, stain,inout2, linein):
    tmp = []
    tmp.append(cardno)
    tmp.append(datetime)
    tmp.append(staname)
    tmp.append(inout1)
    tmp.append(line)
    tmp.append(cardsort)
    tmp.append(datetimein)
    tmp.append(stain)
    tmp.append(inout2)
    tmp.append(linein)
    #print(tmp)
    tables.append(tmp)
    #print(tmp)

def inputStationData(workManStationDict, workManStationList, beginTime, now):
    for weekType in range(0, 2):
        tables = workManStationList[weekType]
        dic = getStationDict(now)
        tmp = []
        tmp.append(beginTime)
        tmp.append(now)
        for stationKey in dic:
            tmp.append(dic[stationKey][0])
            tmp.append(dic[stationKey][1])
            #print(tmp)
            #print(tmp)
        tables.append(tmp)

def isChangeDay(date, lastDay):
    #print("in judge day")
    #print(getDay(date))
    #print(lastDay)
    if getDay(date) != lastDay:
        return True
    else:
        return False

def isChangeWeek(now, lastWeekType):
    #print("in judge week")
    nowWeekType = getWeekType(now)
    if (nowWeekType == 1):
        return False
    elif (nowWeekType == 0 and lastWeekType == 0):
        return False
    else:
        return True

def changeDay(isWorkToday, timesInOneWeek,isWorkMorning, workManMorningData):
    #print("changeday")
    for id in isWorkToday:
        if isWorkToday[id]:
            handelTimesInOneWeekNull(id, timesInOneWeek)
            timesInOneWeek[id] += 1
    initOneDay(isWorkToday)
    initisWorkME(isWorkMorning)
    initisWorkME(workManMorningData)
    return

def fromMorningToNormal(table, tables):
    tables.append(table)
    return

def getMorningData(hashDiction, ABhash):
    table = hashDiction[ABhash]
    stain = table[7]
    staname = table[2]
    datein = table[6]
    date = table[1]
    return stain, staname, datein, date
def changeWeek(timesInOneWeek, isWorkMan):
    #print("changeweek")
    for id in timesInOneWeek:
        if timesInOneWeek[id] >= 3:
            handelisWorkManNull(id, isWorkMan)
            isWorkMan[id] = True
            #print("true: " +str(id))
    initOneWeek(timesInOneWeek)
    return

for week in range(0,2):
        for stationName in stationNameList:
            handleStationNull(stationName, workManStationDict[week])

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
    with open("./sortedData/"+filename, mode='r') as csv_tmp:
        csv_reader = csv.DictReader(csv_tmp,fieldnames=['cardno','payno','datetime','line','staname','inout','cardsort','datetimein','linein','stain'])
        
        for row in csv_reader:
            if first:
                first = False
                beginTime = getHalfHourlyChime(convertDate(row['datetime']))
                lastDay = getDay(row['datetime'])
                lastWeekType = getWeekType(beginTime)
            date = row['datetime']
            now =  getHalfHourlyChime(convertDate(row['datetime']))
            nowType =  getWeekType(convertDate(row['datetime']))
            id = row['cardno']
            staname = row['staname']
            stain = row['stain']
            timeType = isWorkTime(date)
            stationId = row['staname']
            if nowType == 1:
                timeType = 2
#            print(row)
            if stain == '':
                continue
            '''
            if id in isWorkMorning:
                print("id in")
                print(date)
                print(timeType)

            if timeType == 1:
                print(date)
            '''
            if timeType == 0:
                handelIsWorkMENull(id, isWorkMorning)
                handelIsWorkMENull(id, workManMoringData)
                #print(isWorkMorning)
                isWorkMorning[id][getHashAB(stain, staname)] = True
                inputMorningData(workManMoringData[id], getHashAB(stain, staname), row['cardno'],  row['datetime'], row['staname'], row['inout'], row['line'], row['cardsort'],
                                        row['datetimein'], row['stain'],'28', row['linein'])
                #print("hit morning")
            elif timeType == 1 and id in isWorkMorning and getInverseHashAB(stain, staname) in isWorkMorning[id] and isWorkMorning[id][getInverseHashAB(stain, staname)]:
                    #print("hit")
                    handelIsWorkTodayNull(id, isWorkToday)
                    isWorkToday[id] = True
                    handleNull(id, workManNormalDict)
                    inputNormalData(workManNormalDict[id], row['cardno'],  row['datetime'], row['staname'], row['inout'], row['line'], row['cardsort'],
                                        row['datetimein'], row['stain'],'28', row['linein'])
                    if getInverseHashAB(stain, staname) not in workManMoringData[id]:
                        print("fuck")
                    fromMorningToNormal(workManNormalDict[id], workManMoringData[id][getInverseHashAB(stain, staname)])
                    #print("hit")
                    homePlace, workPlace, morningin, morningout = getMorningData(workManMoringData[id], getInverseHashAB(stain, staname))
                    handleNull(id, workManAdvanceDict)
                    inputAdvanceData(workManAdvanceDict[id], row['cardno'], homePlace, workPlace,  row['cardsort'], morningin, morningout, row['datetimein'],  row['datetime'])
                    processHourlyStation(workManStationDict, stationId, now, row['inout'])
            if isChangeDay(date, lastDay):
                print("changeDay")
                changeDay(isWorkToday, timesInOneWeek, isWorkMorning, workManMoringData)
            if isChangeWeek(now, lastWeekType):
                print("changeweek")
                changeWeek(timesInOneWeek, isWorkMan)    
            if now-beginTime >= HALFHOURTIME:
                    inputStationData(workManStationDict, workManStationList, beginTime, now)
                    beginTime = now
                    initDict(workManStationDict)
            lastDay = getDay(date)
            lastWeekType = getWeekType(now)
        csv_tmp.close()

    filename = str(year)+".csv"
    pathName4 = "./data/out/workman/4_chain/"
    if os.path.isdir(pathName4) == False:
        os.mkdir(pathName4)
    with open(pathName4+filename, mode='w', newline='') as csv_to_write:
        csv_writter = csv.writer(csv_to_write, delimiter=',')
        firstRow = [  'cardno', 'homePlace', 'workPlace',  'cardsort', 'morningin', 'morningout', 'datetimein',  'datetimeout']
        csv_writter.writerow(firstRow)
        for key in workManAdvanceDict:
            if key in isWorkMan and isWorkMan[key]:
                tables = workManAdvanceDict[key]
                for row in tables:
                    csv_writter.writerow(row)
        csv_to_write.close()
    pathName5 = "./data/out/workman/5_isChange/"
    if os.path.isdir(pathName5) == False:
        os.mkdir(pathName5)
    for key in workManAdvanceDict:
        if key in isWorkMan and isWorkMan[key]:
            tables = workManAdvanceDict[key]
            #print("hello")
            filename = pathName5+getIsChangeName(tables)+str(year)+".csv";
            with open(filename, mode='a+',newline='') as csv_to_write:
                csv_writter = csv.writer(csv_to_write, delimiter=',')
                for row in tables:
                    csv_writter.writerow(row)
                csv_to_write.close()
    for key in workManAdvanceDict:
        workManAdvanceDict[key] = []


print("----------load finish---------")

'''
for id in isWorkMan:
    print(id)
'''

filename = '(1)原始通勤数据.csv'
with open("./data/out/workman/"+filename, mode='w',newline='') as csv_tmp:
    csv_writter = csv.writer(csv_tmp, delimiter=',')
    firstRow = [ 'cardno', 'datetime', 'staname','inout1', 'line', 'cardsort', 'datetimein', 'stain', 'inout2', 'linein']
    csv_writter.writerow(firstRow)
    for key in workManNormalDict:
        if key in isWorkMan and isWorkMan[key]:
            tables = workManNormalDict[key]
            for row in tables:
                csv_writter.writerow(row)
        
  

lastDay = getDay('20140317055456')
beginTime = convertDate('20140317055456')
lastWeekType = getWeekType(beginTime)
first = True

for year in range(2014, 2020):
    filename = "en_ex_"
    filename += str(year)
    filename += "03.csv"
    with open("./sortedData/"+filename, mode='r') as csv_tmp:
        csv_reader = csv.DictReader(csv_tmp,fieldnames=['cardno','payno','datetime','line','staname','inout','cardsort','datetimein','linein','stain'])
        
        for row in csv_reader:
            if first:
                first = False
                beginTime = getHalfHourlyChime(convertDate(row['datetime']))
            date = row['datetime']
            now =  getHalfHourlyChime(convertDate(row['datetime']))
            nowType =  getWeekType(convertDate(row['datetime']))
            id = row['cardno']
            staname = row['staname']
            stain = row['stain']
            timeType = isWorkTime(date)
            stationId = row['staname']
            if nowType == 1:
                timeType = 2
#            print(row)
            '''
            if id in isWorkMorning:
                print("id in")
                print(date)
                print(timeType)

            if timeType == 1:
                print(date)
            '''
            if (timeType == 1 or timeType == 0) and id in isWorkMan and isWorkMan[id] == True:
                    #print("hit")
                    processHourlyStation(workManStationDict, stationId, now, row['inout'])
                    
            
            if now-beginTime >= HALFHOURTIME:
                    inputStationData(workManStationDict, workManStationList, beginTime, now)
                    beginTime = now
                    initDict(workManStationDict)
        csv_tmp.close()

   


print("----------load finish---------")

        
  




for j in range(0, 2):
    filename = '(3).csv'
#        print(getPeopleName(i))
#        print(getWeekName(j))
    pathName3 = "./data/out/workman/"+getWeekName(j)+"/"
    if os.path.isdir(pathName3) == False:
        os.mkdir(pathName3)
    with open(pathName3+filename, mode='a+', newline='') as csv_tmp:
        csv_writter = csv.writer(csv_tmp, delimiter=',')
        firstRow = [ 'beginTime', 'endTime']
        for key in workManStationDict[j]:
            firstRow.append(key+'in')
            firstRow.append(key+'out')
        csv_writter.writerow(firstRow)
        for row in getStationList(j):
            csv_writter.writerow(row)
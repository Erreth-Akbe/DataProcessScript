import csv
from datetime import datetime
from datetime import timedelta
#总字典
allDict = dict()
#四个字典，分别依次对应通勤人员，老人，残疾人，中小学生的普通出行数据
fourNomalDict = []
#四个字典 同上记录四种人员的出站入站数据
fourAdvanceDict = []
#一个list，其中有两个元素，分别对应：0->工作日，1->周末，用于统计站点进出数据
stationData = []
stationData.append(dict())
stationData.append(dict())

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

def initDict(stationData):
    for dictionary in stationData:
        for data in dictionary:
            dictionary[data] = 0

def checkType(cardsort):
    if cardsort == '1106':
        return 1
    elif cardsort == '1104':
        return 2
    elif cardsort == '1112':
        return 3
    return -1

def getNomalDict(type):
    return fourNomalDict[type]

def getAdvanceDict(type):
    return fourAdvanceDict[type]

def getName(type):
    if type == 1:
        return "old"
    elif type == 2:
        return "disable"
    elif type == 3:
        return "student"

def handleNull(id, dic):
    if id not in dic:
        dic[id] = []


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
    tables.append(tmp)

def inputStationData(tables, staname, starttime, endtime, numbers):
    tmp = []
    tmp.append(staname)
    tmp.append(starttime)
    tmp.append(endtime)
    tmp.append(numbers)

def processHourlyStation(row, stationdata):
    initDict(staiondata)


yearBench = 2014
beginTime = convertDate('20140317055456')
first = True
for i in range(0, 6):
    filename = ""
    filename += "en_ex_"
    filename += str(i+yearBench)
    filename += "03.csv"
    with open("./testdata/"+filename, mode='r') as csv_tmp:
        csv_reader = csv.DictReader(csv_tmp,fieldnames=['cardno','payno','datetime','line','staname','inout','cardsort','datetimein','linein','stain'])
        
        for row in csv_reader:
            #print(convertDate(row['datetime']))
            # process all
            if first:
                first = False
                beginTime = getHourlyChime(convertDate(row['datetime']))
            now =  getHourlyChime(convertDate(row['datetime']))
            #print(now)
            if now-beginTime > ONEHOURTIME:
                print("wuhu")
            else:
                print("aha")
                '''
            if getHourlyChime(convertDate(row['datetime']))  == beginTime:
                print("yes"+str(getHourlyChime(convertDate(row['datetime']))))
            if getHourlyChime(convertDate(row['datetime']))  != beginTime:
                print("nononono"+str(getHourlyChime(convertDate(row['datetime']))))
                '''
            id = row['cardno']
            handleNull(id, allDict)

            # process three types
            type = checkType(row['cardsort'])
            if type != -1 :
                handleNull(id, getNomalDict(type))
                inputNomalData(getNomalDict(type)[id], row['cardno'], row['datetime'], row['line'], row['staname'], row['inout'], row['cardsort'])
                if row['stain'] != '':
                    inputAdvanceData(getNomalDict(type)[id], row['cardno'],  row['datetime'], row['staname'], row['line'], 
                                        row['datetimein'], row['stain'], row['linein'], int(row['datetime'])-int(row['datetimein']), row['cardsort'])
        
        csv_tmp.close()
print("----------load finish---------")

for i in range(1, 4):
    filename = '(1).csv'
    with open("./data/out/"+getName(i)+"/"+filename, mode='w') as csv_tmp:
        csv_writter = csv.writer(csv_tmp, delimiter=',')
        firstRow = ['cardno', 'datetime', 'line', 'staname', 'inout', 'cardsort']
        csv_writter.writerow(firstRow)
        for key in getNomalDict(i):
            tables = getNomalDict(i)[key]
            for row in tables:
                csv_writter.writerow(row)
        
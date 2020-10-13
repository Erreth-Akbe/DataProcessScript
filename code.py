import csv

#总字典
allDict = dict()
#四个字典，分别依次对应通勤人员，老人，残疾人，中小学生的普通出行数据
fourNomalDict = []
#四个字典 同上记录出站入站
fourAdvanceDict = []
for i in range(0, 4):
    fourNomalDict.append(dict())
    fourAdvanceDict.append(dict())

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
    print(tmp)
    tables.append(tmp)


yearBench = 2014
for i in range(0, 6):
    filename = ""
    filename += "en_ex_"
    filename += str(i+yearBench)
    filename += "03.csv"
    with open("./testdata/"+filename, mode='r') as csv_tmp:
        csv_reader = csv.DictReader(csv_tmp,fieldnames=['cardno','payno','datetime','line','staname','inout','cardsort','datetimein','linein','stain'])
        
        for row in csv_reader:
            
            # process all
            id = row['cardno']
            handleNull(id, allDict)

            # process three types
            type = checkType(row['cardsort'])
            if type != -1 :
                handleNull(id, getNomalDict(type))
                inputNomalData(getNomalDict(type)[id], row['cardno'], row['datetime'], row['line'], row['staname'], row['inout'], row['cardsort'])
                if row['stain'] is not '':
                    inputAdvanceData(getNomalDict(type)[id], row['cardno'],  row['datetime'], row['staname'], row['line'], 
                                        row['datetimein'], row['stain'], row['linein'], int(row['datetime'])-int(row['datetimein']), row['cardsort'])
        
        csv_tmp.close()
print("load finish")

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
        
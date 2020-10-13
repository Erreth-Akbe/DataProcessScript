import csv

files = []
yearBench = 2014
for i in range(0, 6):
    filename = ""
    filename += "en_ex_"
    filename += str(i+yearBench)
    filename += "03.csv"
    lines = 0
    tmp = []
    with open("./data/"+filename, mode='r') as csv_tmp:
        csv_reader = csv.reader(csv_tmp)
        for row in csv_reader:
            tmp.append(row)
            lines += 1
            if lines > 10000: 
                break
        csv_tmp.close()
    files.append(tmp)
print("load finish")

for i in range(0, 6):
    filename = ""
    filename += "en_ex_"
    filename += str(i+yearBench)
    filename += "03.csv"
    with open("./testdata/"+filename, mode='w') as csv_tmp:
        csv_writter = csv.writer(csv_tmp, delimiter=',')
        for row in files[i]:
            csv_writter.writerow(row)
        
        
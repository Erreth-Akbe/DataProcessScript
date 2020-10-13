import pandas as pd

csvframe = []
bench = 2014
for i in range(0, 6):
    filename = ""
    filename += "en_ex_"
    filename += str(i+bench)
    filename += "03.csv"
    print(filename)
    tmp = pd.read_csv("./data/"+filename)
    csvframe.append(tmp)
print(csvframe)
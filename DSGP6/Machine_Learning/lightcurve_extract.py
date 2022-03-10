import lightkurve as lk
from csv import reader

data_array = []
# open file in read mode
with open('/Users/thayalanpraveen/Documents/GitHub/PlanetHunters/DSGP6/Machine_Learning/Dataset_v2.csv', 'r') as read_obj:
    # pass the file object to reader() to get the reader object
    csv_reader = reader(read_obj)
    header = next(csv_reader)
    for r in range(1,272):
           next(csv_reader)
    index = 0
    # Iterate over each row in the csv using reader object
    for row in csv_reader:
        # row variable is a list that represents a row in csv
        try:
            search_result = lk.search_lightcurve(row[0])
            lc = search_result[0].download()
            x_data = []
            y_data = []
            y_val = 0
            x = lc.time
            print(index)
            if len(x) < 1627 :
                index = index + 1
                y = lc.flux
                for i in range(1,len(x)):
                    x_data.append(x[i].value)
                    y_val = float(y[i].value)
                    y_data.append(y_val)
                data_array.append([row[3],row[0],row[1],row[2],x_data,y_data])
                if index == 500 :
                    break
        except :
            print("download error")

import csv  

header = ['row','kepid', 'koi_disposition', 'koi_score','time','flux']

with open('/Users/thayalanpraveen/Documents/GitHub/PlanetHunters/DSGP6/Machine_Learning/lc_data_update.csv', 'w', encoding='UTF8') as f:
    writer = csv.writer(f)

    # write the header
    writer.writerow(header)

    # write the data
    for k in range(0,index):
        writer.writerow(data_array[k])

    
        


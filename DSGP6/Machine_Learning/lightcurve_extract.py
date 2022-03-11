import lightkurve as lk
from csv import reader
import csv  

# open file in read mode
with open('/Users/thayalanpraveen/Documents/GitHub/PlanetHunters/DSGP6/Machine_Learning/Dataset_v2.csv', 'r') as read_obj:
    with open('/Users/thayalanpraveen/Documents/GitHub/PlanetHunters/DSGP6/Machine_Learning/lc_data_update.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        # pass the file object to reader() to get the reader object
        csv_reader = reader(read_obj)
        next(csv_reader)
        for r in range(1,3119):
            next(csv_reader)
        index = 0
        # Iterate over each row in the csv using reader object
        for row in csv_reader:
            # row variable is a list that represents a row in csv
            try:
                search_result = lk.search_lightcurve(row[0])
                lc = search_result[0].download()
                y_data = []
                y_val = 0
                y = lc.flux
                print(index)
                if len(y) < 1627 :
                    index = index + 1
                    y = lc.flux
                    for i in range(1,len(y)):
                        y_val = float(y[i].value)
                        y_data.append(y_val)
                    data = [row[3],row[0],row[1],row[2],y_data]
                    writer.writerow(data)
            except :
                print("download error")

    
        


import lightkurve as lk
from csv import reader
import joblib

# open file in read mode
with open('/Users/thayalanpraveen/Documents/GitHub/PlanetHunters/DSGP6/Machine_Learning/Dataset_v2.csv', 'r') as read_obj:
    # pass the file object to reader() to get the reader object
    csv_reader = reader(read_obj)
    next(csv_reader)
    #for r in range(1,3119):
    #    next(csv_reader)
    index = 0
    search = False
    Dataset = []
    # Iterate over each row in the csv using reader object
    for row in csv_reader:
        # row variable is a list that represents a row in csv
        data = [row[0],row[1]]
        try:
            if search == False:
                search_result = lk.search_lightcurve(row[0])
                search = True
                y_val = []

            if search == True:
                for x in range(0,17):
                    try:
                        lc = search_result[x].download() 
                        y = lc.flux
                        for i in range(1,len(y)):
                            data.append(float(y[i].value))
                    except :
                        pass
                    
                Dataset.append(data)
                search = False
                index = index + 1
                print(index)
                joblib.dump(Dataset, 'Dataset.joblib')

        except :
            print("download error")


    
        


import lightkurve as lk
from csv import reader
import joblib
import os
import sys

try:
    array = joblib.load('Dataset.joblib')
    joblib.dump(array, 'Dataset1.joblib')

except:
    array = joblib.load('Dataset1.joblib')
    print("Dataset.joblib corrupted,using Dataset1.joblib")
    joblib.dump(array, 'Dataset.joblib')


# open file in read mode
with open(os.path.join(sys.path[0],'Dataset_v2.csv'), 'r') as read_obj:
    # pass the file object to reader() to get the reader object
    csv_reader = reader(read_obj)
    next(csv_reader)
    index = len(array)
    for r in range(0,index):
        next(csv_reader)
    search = False
    Dataset = array
    dump_i = 0
    # Iterate over each row in the csv using reader object
    for row in csv_reader:
        # row variable is a list that represents a row in csv
        data = [row[0],row[1]]
        lc_array = []
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
                        lc_array.append(y)
                    except :
                        pass
                for x in range(0,len(lc_array)):
                    for i in range(1,len(y),10):
                                try:
                                    data.append(float(lc_array[x][i].value))
                                except:
                                    pass
                Dataset.append(data)
                search = False
                index = index + 1
                print(index)
                dump_i = dump_i + 1
                if dump_i == 10 :
                    dump_i = 0
                    print("Dumping")
                    joblib.dump(Dataset, 'Dataset.joblib')
                    joblib.dump(Dataset, 'Dataset1.joblib')
                    print("Dump Complete")
                
        except :
            print("download error")
            index = index + 1
            print(index)



    
        


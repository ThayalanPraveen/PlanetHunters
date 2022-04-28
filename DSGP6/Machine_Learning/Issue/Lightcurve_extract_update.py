import lightkurve as lk
from csv import reader
import joblib
import os
import sys
import warnings

try:
    array = joblib.load('Dataset.joblib')
    joblib.dump(array, 'Dataset1.joblib')

except:
    array = joblib.load('Dataset1_test.joblib')
    print("Dataset.joblib corrupted,using Dataset1.joblib")
    joblib.dump(array, 'Dataset_test.joblib')

D_error = 0

# open file in read mode
with open(os.path.join(sys.path[0],'Dataset_v2.csv'), 'r') as read_obj:
    # pass the file object to reader() to get the reader object
    csv_reader = reader(read_obj)
    next(csv_reader)
    index = len(array)
    for r in range(0,index):
        next(csv_reader)
    Dataset = array
    dump_i = 0
    # Iterate over each row in the csv using reader object
    for row in csv_reader:
        error = 0
        # row variable is a list that represents a row in csv
        data = [row[0],row[1]]
        try:
            y = []
            search_result = lk.search_lightcurve(row[0])
            lc = search_result.download_all()
            error = error + 1

            for j in range(0,len(lc)):
                y.extend(lc[j].flux)
            
            for i in range(1,len(y),10):
                try:
                    data.append(float(y[i].value))
                except:
                    pass
            
            error = error + 1

            Dataset.append(data)
            index = index + 1
            print(index)
            dump_i = dump_i + 1
            if dump_i == 10 :
                dump_i = 0
                print("Dumping")
                joblib.dump(Dataset, 'Dataset_test.joblib')
                joblib.dump(Dataset, 'Dataset1_test.joblib')
                print("Dump Complete")
                
        except :
            D_error = D_error +1
            print("Download error! #" + D_error)
            index = index + 1
            print(index)



    
        


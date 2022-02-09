## file to test lightkurve functions

import numpy as np
import lightkurve as lk

def search_star(target_name,target_author):
    if target_name == '' or target_author == '':
        print("No Target Name input/ Author selected")
        return False
    else:
        search_result = lk.search_lightcurve(target_name, author=target_author)
        return search_result

def search_filter(identifier,value,target_name,target_author):
        search_result = lk.search_lightcurve(target_name, author=target_author)
        
        if identifier == '' or value == '':
            print("Please Select Identifier & Input valid Value")
            return 0,0
        else:
            try:
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                    value = str()
                    filter = np.where(search_result.table[identifier] == value)[0]
                    filtered = True
                    return search_result[filter] , filtered
                else:
                    filter = np.where(search_result.table[identifier] == int(value))[0]
                    filtered = True
                    return search_result[filter] , filtered
            except:
                filter = np.where(search_result.table[identifier] == int(value))[0]
                filtered = True
                return search_result[filter] , filtered


out = search_star("TIC 145241359","QLP") ## working search function
print(out)
filter = search_filter("year","2018","TIC 145241359","QLP") ## working filter function
filter2 = search_filter("year","2019","TIC 145241359","QLP") ## working filter function
print(filter[0])
print(filter2[0])
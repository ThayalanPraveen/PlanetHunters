import sys
## file to test lightkurve functions

import numpy as np
import lightkurve as lk

## Search function
def search_star(target_name):
    if target_name == '':
        print("No Target Name input")
        return False
    else:
        search_result = lk.search_lightcurve(target_name)
        filtered = False
        return search_result , filtered , 0

## Reset function
def reset_search(target_name):
    search_result = lk.search_lightcurve(target_name)
    filtered = False
    return search_result, filtered , 0

## search filter function
def search_filter(identifier,value,target_name):
        search_result = lk.search_lightcurve(target_name)
        
        if identifier == '' or value == '':
            print("Please Select Identifier & Input valid Value")
            return 0,0,0
        else:
            try:
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                    value = str()
                    filter = np.where(search_result.table[identifier] == value)[0]
                    filtered = True
                    return search_result , filtered , filter
                else:
                    filter = np.where(search_result.table[identifier] == int(value))[0]
                    filtered = True
                    return search_result , filtered , filter
            except:
                filter = np.where(search_result.table[identifier] == int(value))[0]
                filtered = True
                return search_result , filtered , filter

## select star function
def select_star(hash_id,search_result,filtered,filter):
    if hash_id == '':
        print("Input valid #") ## finish validation
        return 0,0,0
    else:
        if filtered == True:
            lc = search_result[filter[int(hash_id)]].download()
        else:
            lc = search_result[int(hash_id)].download()
        return lc

## show search results function        
def show_search_results(search_results,filtered,filter):
    if filtered == False :
        return search_results
    else:
        return search_results[filter]

out = search_star("TIC 441420236") ## working search function
search = select_star(0,out,filtered=False,filter= 0)
out2 = show_search_results(search,False,0)
print(out2[0])



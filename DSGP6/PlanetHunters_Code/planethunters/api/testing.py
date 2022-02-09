## file to test lightkurve functions

import numpy as np
import lightkurve as lk

## Search function
def search_star(target_name,target_author):
    if target_name == '' or target_author == '':
        print("No Target Name input/ Author selected")
        return False
    else:
        search_result = lk.search_lightcurve(target_name, author=target_author)
        filtered = False
        return search_result , filtered , 0

## Reset function
def reset_search(target_name,target_author):
    search_result = lk.search_lightcurve(target_name, author=target_author)
    filtered = False
    return search_result, filtered , 0

## search filter function
def search_filter(identifier,value,target_name,target_author):
        search_result = lk.search_lightcurve(target_name, author=target_author)
        
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
        print("Input valid #")
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

out = search_star("TIC 145241359","QLP") ## working search function
filter = search_filter("year","2018","TIC 145241359","QLP") ## working filter function
print(show_search_results(filter[0],filter[1],filter[2])) ## working show function
filter2 = search_filter("year","2019","TIC 145241359","QLP") ## working filter function
print(show_search_results(filter2[0],filter2[1],filter2[2])) ## working show function
selected_star = select_star(0,filter2[0],filter2[1],filter2[2]) ## working select function
print(selected_star)


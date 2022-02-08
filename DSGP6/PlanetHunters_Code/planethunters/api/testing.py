## file to test lightkurve functions


import lightkurve as lk
def search_star(target_name,target_author):
    if target_name == '' or target_author == '':
        print("No Target Name input/ Author selected")
        return False
    else:
        search_result = lk.search_lightcurve(target_name, author=target_author)
        return search_result

out = search_star("TIC 145241359","QLP")
print(out.target_name)
if (out == "SearchResult containing 0 data products.") :
    print("statement true")
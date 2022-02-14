import pandas as pd

data = pd.read_csv(r'/Users/thayalanpraveen/Documents/GitHub/PlanetHunters/DSGP6/Machine_Learning/Dataset.csv')
##data = pd.read_csv(r'/Users/thayalanpraveen/Documents/GitHub/PlanetHunters/DSGP6/Machine_Learning/Dataset.csv') Kanishka dataset location
##data = pd.read_csv(r'/Users/thayalanpraveen/Documents/GitHub/PlanetHunters/DSGP6/Machine_Learning/Dataset.csv') Hamdaan dataset location
##data = pd.read_csv(r'/Users/thayalanpraveen/Documents/GitHub/PlanetHunters/DSGP6/Machine_Learning/Dataset.csv') Maryam dataset location
print(data)

## statistics of dataset columns
data_stats = data.describe()
print(data_stats) 


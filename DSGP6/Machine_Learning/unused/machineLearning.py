import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

raw_data = pd.read_csv(r'/Users/thayalanpraveen/Documents/GitHub/PlanetHunters/DSGP6/Machine_Learning/Dataset.csv')
##data = pd.read_csv(r'/Users/thayalanpraveen/Documents/GitHub/PlanetHunters/DSGP6/Machine_Learning/Dataset.csv') Kanishka dataset location
##data = pd.read_csv(r'/Users/thayalanpraveen/Documents/GitHub/PlanetHunters/DSGP6/Machine_Learning/Dataset.csv') Hamdaan dataset location
##data = pd.read_csv(r'/Users/thayalanpraveen/Documents/GitHub/PlanetHunters/DSGP6/Machine_Learning/Dataset.csv') Maryam dataset location
print(raw_data)

## statistics of dataset columns
data_stats = raw_data.describe()
print(data_stats) 

# finding number of missing values
print(raw_data.isnull().sum())

##removing all columns with NaN Values
##remove_nan_values = data.dropna(axis=1)
##print(remove_nan_values)
##remove_nan_values.info()

## deleting the kepler_name column
## data = data.drop("kepler_name", axis=1)

## columns not needed
drop_col = ['koi_pdisposition', 'koi_tce_plnt_num', 'koi_tce_delivname', 'kepler_name']

# gonna iterate through the columns of the raw data to add the uncertainty/error ones to the drop-list (koi_pond)
cols = raw_data.columns

# dropping the error columns, every column with 'err' in the name.
for c in cols:
    if 'err' in c:
        drop_col.append(c)

# finalize changes, but hold on to the raw data in case needed later
data = raw_data.drop(drop_col, axis = 1)

print("Dropped:\n\n", drop_col)
print(f"\nYour dataset had {raw_data.shape[1]} columns.\nIt now has {data.shape[1]} columns.")


## replacing all missing numerical values with mean
##data.fillna(data.mean(), inplace=True)

##print(data.isnull().sum())

data = pd.pivot_table(data=data,index=['koi_disposition'], columns=['kepid'])
data.dropna()
print(data)


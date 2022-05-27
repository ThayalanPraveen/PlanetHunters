import lightkurve as lk
import numpy as np
import pickle
import os
import sys
import pandas as pd
import requests

data_period = 13.0339
data_epoch = 1530.34
data_duration = 0.2


lcs = lk.search_lightcurve('TIC 145241359',author='QLP',cadence='long').download_all()
print(lcs.author)
lc = lcs.stitch()
lc_clean = lc.remove_outliers(sigma=20, sigma_upper=4)
temp_fold = lc_clean.fold(data_period, epoch_time=data_epoch)
fractional_duration = (data_duration / 24.0) / data_period
phase_mask = np.abs(temp_fold.phase.value) < (fractional_duration * 1.5)
transit_mask = np.in1d(lc_clean.time.value, temp_fold.time_original.value[phase_mask])
lc_flat, trend_lc = lc_clean.flatten(return_trend=True, mask=transit_mask)
lc_fold = lc_flat.fold(data_period, epoch_time=data_epoch)
lc_global = lc_fold.bin(time_bin_size=0.005).normalize() - 1
lc_global = (lc_global / np.abs(lc_global.flux.min()) ) * 2.0 + 1
lc_global.scatter()

phase_mask = (lc_fold.phase > -4*fractional_duration) & (lc_fold.phase < 4.0*fractional_duration)
lc_zoom = lc_fold[phase_mask]
lc_local = lc_zoom.bin(time_bin_size=0.0005).normalize() - 1
lc_local = (lc_local / np.abs(np.nanmin(lc_local.flux)) ) * 2.0 + 1

array_all = []

global_lc = []
local_lc = []

for x in range(0,len(lc_global.flux),10):
    try:
        global_lc.append(lc_global.flux[x])
    except:
        break

for x in range(0,len(lc_local.flux)):
    try:
        local_lc.append(lc_local.flux[x])
    except:
        break

print(len(global_lc))
print(len(local_lc))

with open(os.path.join(sys.path[0],'RFM_G_model_pkl') , 'rb') as f:
    global_model = pickle.load(f)

with open(os.path.join(sys.path[0],'RFM_L_model_pkl') , 'rb') as f:
    local_model = pickle.load(f)

#-----------------------------------------

for i in range(len(global_lc),17134):
    global_lc.append(-999)

df_global = pd.DataFrame(global_lc)
df_global = df_global.fillna(-999)

global_lc = []
for x in df_global[0] :
    global_lc.append(x)

print("Global Results:")
print(global_model.predict([global_lc]))

#------------------------------------------

for i in range(len(local_lc),2773):
    local_lc.append(-999)

df_local = pd.DataFrame(local_lc)
df_local = df_local.fillna(-999)

local_lc = []
for x in df_local[0] :
    local_lc.append(x)

print("Local Results:")
print(local_model.predict([local_lc]))


import csv
import os
import sys
import lightkurve as lk
import numpy as np
import pickle
import pandas as pd


TIC_Array = []
VerifiedTicId = []
VerifiedTicIdScore = []
errorCount = 0

def ml_predict(ticId,author):
    global errorCount
    try:
        target_search_result = lk.search_lightcurve(ticId,cadence='long')
        lightcurve = target_search_result[0].download()

        period = np.linspace(1, 20, 10000)
        bls = lightcurve.to_periodogram(method='bls', period=period, frequency_factor=500)
        bls_period = bls.period_at_max_power
        bls_transit = bls.transit_time_at_max_power
        bls_duration = bls.duration_at_max_power
        
        data_period = bls_period.value
        data_epoch = bls_transit.value
        data_duration = bls_duration.value

        lcs = lk.search_lightcurve(ticId,cadence='long').download_all()
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
        
        with open(os.path.join(sys.path[0],'Models/RFM_G_model_pkl') , 'rb') as f:
            global_model = pickle.load(f)

        with open(os.path.join(sys.path[0],'Models/RFM_L_model_pkl') , 'rb') as f:
            local_model = pickle.load(f)

        #-----------------------------------------

        for i in range(len(global_lc),17134):
            global_lc.append(-999)

        df_global = pd.DataFrame(global_lc)
        df_global = df_global.fillna(-999)

        global_lc = []
        for x in df_global[0] :
            global_lc.append(x)

        for i in range(len(local_lc),2773):
            local_lc.append(-999)

        df_local = pd.DataFrame(local_lc)
        df_local = df_local.fillna(-999)

        local_lc = []
        for x in df_local[0] :
            local_lc.append(x)

    
        g = global_model.predict([global_lc])
        l = local_model.predict([local_lc])

        if g[0] ==1 and l[0] ==1 :
            VerifiedTicId.append(ticId)
            VerifiedTicIdScore.append(1)
        elif g[0]==1 or l[0]==1 :
            VerifiedTicId.append(ticId)
            VerifiedTicIdScore.append(0.5)
        else :
            VerifiedTicId.append(ticId)
            VerifiedTicIdScore.append(0)
    except:
        errorCount = errorCount + 1
        print("Couldn't Stitch")

ml_predict("TIC 145241359","QLP")

'''
with open(os.path.join(sys.path[0],'CTLv8.csv')) as csv_file:
    csv_reader = csv.reader(csv_file)
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print("column names")
            line_count += 1
        else:
            TIC_Array.append("TIC "+ row[0])
            print(TIC_Array[line_count-1])
            ml_predict(TIC_Array[line_count-1],"TESS")
            line_count +=1
    print("Processed "+str(line_count)+" lines.")
    print("error count : "+ str(errorCount))
    '''


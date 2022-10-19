from locale import normalize
import lightkurve as lk
y = []
T_name = 'TIC 145241359'
search_result = lk.search_lightcurve(T_name)
lc = search_result.download_all() 

for j in range(0,len(lc)):
    y.extend(lc[j].flux)

print(y[2000])   

'''
lc = lk.LightCurveCollection.stitch(lc)

lc = lc.normalize().remove_nans().remove_outliers() 
pg = lc.to_periodogram(normalization='psd', minimum_frequency=100, maximum_frequency=800)  

seismology = pg.flatten().to_seismology()  
nm = seismology.estimate_numax()
d = seismology.estimate_deltanu()
r = seismology.estimate_radius(teff=5650,numax=nm,deltanu = d) 
m = seismology.estimate_mass(teff=5650,numax=nm,deltanu = d) 
g = seismology.estimate_logg(teff=5650,numax=nm) 
print(r)
print(m)
print(g)

'''

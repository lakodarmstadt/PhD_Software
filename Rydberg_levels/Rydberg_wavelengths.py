#import numpy as np
from arc import *
import pandas as pd

atom = Rubidium()

#D1 line data
print('D1 line: 5S_1/2 -> 5P_1/2')
print('%.3f nm' % (atom.getTransitionWavelength(5,0,0.5,5,1,0.5)*1e9))
print('%.3f THz' % (atom.getTransitionFrequency(5,0,0.5,5,1,0.5)*1e-12))

#D2 line data
print('D2 line: 5S_1/2 -> 5P_3/2')
print('%.3f nm' % (atom.getTransitionWavelength(5,0,0.5,5,1,1.5)*1e9))
print('%.3f THz' % (atom.getTransitionFrequency(5,0,0.5,5,1,1.5)*1e-12))

nmin=28
nmax=300



wavelength_list_D1=[[n,atom.getTransitionWavelength(5,1,0.5,n,0,0.5)*1e9,atom.getTransitionWavelength(5,1,0.5,n,1,0.5)*1e9,atom.getTransitionWavelength(5,1,0.5,n,1,1.5)*1e9,atom.getTransitionWavelength(5,1,0.5,n,2,1.5)*1e9,atom.getTransitionWavelength(5,1,0.5,n,2,2.5)*1e9] for n in range(nmin,nmax)]
fund_wavelength_list_D1=[[n,a*2,b*2,c*2,d*2,e*2] for [n,a,b,c,d,e] in wavelength_list_D1]
df_D1=pd.DataFrame(fund_wavelength_list_D1, columns=['n','nS12','nP12','nP32','nD32','nD52'])
#df_D1.to_csv('Transitionwavelengths_D1.csv')

wavelength_list_D2=[[n,atom.getTransitionWavelength(5,1,1.5,n,0,0.5)*1e9,atom.getTransitionWavelength(5,1,1.5,n,1,0.5)*1e9,atom.getTransitionWavelength(5,1,1.5,n,1,1.5)*1e9,atom.getTransitionWavelength(5,1,1.5,n,2,1.5)*1e9,atom.getTransitionWavelength(5,1,1.5,n,2,2.5)*1e9] for n in range(nmin,nmax)]
fund_wavelength_list_D2=[[n,a*2,b*2,c*2,d*2,e*2] for [n,a,b,c,d,e] in wavelength_list_D2]
df_D2=pd.DataFrame(fund_wavelength_list_D2, columns=['n','nS12','nP12','nP32','nD32','nD52'])
#df_D2.to_csv('Transitionwavelengths_D2.csv')

print(df_D1.min(),df_D1.max())
print(df_D2.min(),df_D2.max())

# Note: Convert list into dataframe and learn about dataframes 
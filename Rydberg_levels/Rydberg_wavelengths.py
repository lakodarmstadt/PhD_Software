#import numpy as np
from arc import *
import pandas as pd

atom = Rubidium()

# D1 line data
print('D1 line: 5S_1/2 -> 5P_1/2')
print('%.3f nm' % (atom.getTransitionWavelength(5, 0, 0.5, 5, 1, 0.5) * 1e9))
print('%.3f THz' % (atom.getTransitionFrequency(5, 0, 0.5, 5, 1, 0.5) * 1e-12))

# D2 line data
print('D2 line: 5S_1/2 -> 5P_3/2')
print('%.3f nm' % (atom.getTransitionWavelength(5, 0, 0.5, 5, 1, 1.5) * 1e9))
print('%.3f THz' % (atom.getTransitionFrequency(5, 0, 0.5, 5, 1, 1.5) * 1e-12))

nmin = 28
nmax = 300


# Wavelength lists for Rydberg transition:

wavelength_list_D1 = [[n, atom.getTransitionWavelength(5, 1, 0.5, n, 0, 0.5) * 1e9, atom.getTransitionWavelength(5, 1, 0.5, n, 1, 0.5) * 1e9, atom.getTransitionWavelength(5, 1, 0.5, n, 1, 1.5) * 1e9, atom.getTransitionWavelength(5, 1, 0.5, n, 2, 1.5) * 1e9, atom.getTransitionWavelength(5, 1, 0.5, n, 2, 2.5) * 1e9] for n in range(nmin, nmax)]
fund_wavelength_list_D1 = [[n, a * 2, b * 2, c * 2, d * 2, e * 2] for [n, a, b, c, d, e] in wavelength_list_D1]
df_D1_wavelength = pd.DataFrame(fund_wavelength_list_D1, columns=['n', 'nS12', 'nP12', 'nP32', 'nD32', 'nD52'])
# df_D1_wavelength.to_csv('Transitionwavelengths_D1.csv')

wavelength_list_D2 = [[n, atom.getTransitionWavelength(5, 1, 1.5, n, 0, 0.5) * 1e9, atom.getTransitionWavelength(5, 1, 1.5, n, 1, 0.5) * 1e9, atom.getTransitionWavelength(5, 1, 1.5, n, 1, 1.5) * 1e9, atom.getTransitionWavelength(5, 1, 1.5, n, 2, 1.5) * 1e9, atom.getTransitionWavelength(5, 1, 1.5, n, 2, 2.5) * 1e9] for n in range(nmin, nmax)]
fund_wavelength_list_D2 = [[n, a * 2, b * 2, c * 2, d * 2, e * 2] for [n, a, b, c, d, e] in wavelength_list_D2]
df_D2_wavelength = pd.DataFrame(fund_wavelength_list_D2, columns=['n', 'nS12', 'nP12', 'nP32', 'nD32', 'nD52'])
# df_D2_wavelength.to_csv('Transitionwavelengths_D2.csv')

print(df_D1_wavelength.min(), df_D1_wavelength.max())
print(df_D2_wavelength.min(), df_D2_wavelength.max())

# Frequency lists for Rydberg transition:

frequency_list_D1 = [[n, atom.getTransitionFrequency(5, 1, 0.5, n, 0, 0.5), atom.getTransitionFrequency(5, 1, 0.5, n, 1, 0.5), atom.getTransitionFrequency(5, 1, 0.5, n, 1, 1.5), atom.getTransitionFrequency(5, 1, 0.5, n, 2, 1.5), atom.getTransitionFrequency(5, 1, 0.5, n, 2, 2.5)] for n in range(nmin, nmax)]
fund_frequency_list_D1 = [[n, a / 2, b / 2, c / 2, d / 2, e / 2] for [n, a, b, c, d, e] in frequency_list_D1]
df_D1_frequency = pd.DataFrame(fund_frequency_list_D1, columns=['n', 'nS12', 'nP12', 'nP32', 'nD32', 'nD52'])
df_D1_frequency.to_csv('Transitionfrequencies_D1.csv')

frequency_list_D2 = [[n, atom.getTransitionFrequency(5, 1, 1.5, n, 0, 0.5), atom.getTransitionFrequency(5, 1, 1.5, n, 1, 0.5), atom.getTransitionFrequency(5, 1, 1.5, n, 1, 1.5), atom.getTransitionFrequency(5, 1, 1.5, n, 2, 1.5), atom.getTransitionFrequency(5, 1, 1.5, n, 2, 2.5)] for n in range(nmin, nmax)]
fund_frequency_list_D2 = [[n, a / 2, b / 2, c / 2, d / 2, e / 2] for [n, a, b, c, d, e] in frequency_list_D2]
df_D2_frequency = pd.DataFrame(fund_frequency_list_D2, columns=['n', 'nS12', 'nP12', 'nP32', 'nD32', 'nD52'])
df_D2_frequency.to_csv('Transitionfrequencies_D2.csv')

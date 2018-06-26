# import section:
import scipy.constants
import numpy as np

# units:
pico = 1e-12
nano = 1e-9
micro = 1e-6
milli = 1e-3
kilo = 1e3
Mega = 1e6
Giga = 1e9

# Scientific constants:

c = scipy.constants.c

# Important functions:


def sellmeier_equation_UVFS(wavelength):
    # Convert wavelength into um:
    wavelength = wavelength * 1e6
    n_squared = (0.6961663 * wavelength**2) / (wavelength**2 - 0.0684043**2) + (0.4079426 * wavelength**2) / (wavelength**2 - 0.1162414**2) + (0.8974794 * wavelength**2) / (wavelength**2 - 9.896161**2) + 1
    return np.sqrt(n_squared)


def beam_displacement(t, n1, n2, alpha):
    '''
    t: thickness of plate
    n1: index of refraction outside
    n2: index of refraction material
    alpha: angle of incidence (in degree)
    '''
    # Cenvert angle in degree to radians:
    alpha_rad = alpha / 360 * 2 * np.pi
    d = t * np.sin(alpha_rad) * (1 - (np.cos(alpha_rad)) / (np.sqrt((n2 / n1)**2 - np.sin(alpha_rad)**2)))
    return d

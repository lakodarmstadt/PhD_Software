# Import section
import scipy.constants
import numpy as np


# Definitions
micro = 1e-6
nano = 1e-9
c = scipy.constants.c

# Class definitions:


class cavity:
    def __init__(self, length, R1, R2, n, wavelength):
        self.length = length
        self.R1 = R1  # Reflectivity of first mirror
        self.R2 = R2  # Reflectivity second mirror
        self.n = n

    def FSR(self):
        return c / (2 * self.length * self.n)

    def Finesse(self):
        F = (scipy.constants.pi * (self.R1 * self.R2)**(1 / 4)) / (1 - np.sqrt(self.R1 * self.R2))
        return F

    def Coeff_of_Finesse(self):
        F = 4 * np.sqrt(self.R1 * self.R2) / ((1 - np.sqrt(self.R1 * self.R2))**2)
        return F

    def linewidth_FWHM(self):
        FWHM = self.FSR() / self.Finesse()
        return FWHM

    def max_Transmission(self):
        T_max = 1 / (1 + self.Coeff_of_Finesse())
        return T_max

    def Internal_Intensity(self, I_0):
        I = I_0 * (1 + np.sqrt(self.R1 * self.R2) + 2 * (self.R1 * self.R2)**(1 / 4)) / (1 - np.sqrt(self.R1 * self.R2))
        return I


R_780 = 0.999908
R_960 = 0.99985
lambda_780 = 780 * nano
lambda_960 = 960 * nano
n_vac = 1

SLS_Cavity_780 = cavity(0.0985, R_780, R_780, n_vac, lambda_780)
SLS_Cavity_960 = cavity(0.1, R_960, R_960, n_vac, lambda_960)
print('The FSR for 780nm is ' + str(SLS_Cavity_780.FSR()))
print(SLS_Cavity_780.Finesse())
print(SLS_Cavity_780.linewidth_FWHM())
print(SLS_Cavity_780.max_Transmission())
print(SLS_Cavity_780.Internal_Intensity(10 * micro))
print(SLS_Cavity_780.R1)

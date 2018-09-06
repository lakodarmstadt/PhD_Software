# Import section:
import sys
import math
sys.path.append('/home/lars/Dokumente/Lars_Kohfahl/Studium/PhD/PhD_Software')
from basic_definitions import *
from arc import *

atom = Rubidium85()
# Functions section:


def wavelength_to_frequency_converter(wavelength_list):
    freq_list = [c / Lambda for Lambda in wavelength_list]
    return freq_list


def frequency_to_wavelength_converter(frequency_list):
    wavelength_list = [c / nu for nu in frequency_list]
    return wavelength_list


def cavity_resonance_list(FSR, example_resonance_frequency, n):
    '''cavity_resonance_list(FSR, example_resonance_frequency, n)    function to calculate the n nearest resonances with respect to the example_resonance_frequency given the cavity FSR.'''

    resonance_list = [example_resonance_frequency + n * FSR for n in range(-n, n + 1)]
    return resonance_list


def nearest_cavity_resonance(frequency, FSR, example_resonance_frequency, unit=" Hz "):
    FSR_diff = (frequency - example_resonance_frequency) / FSR
    if abs(FSR_diff % 1) <= 0.55:
        resonance_1 = example_resonance_frequency + math.floor(FSR_diff) * FSR
        resonance_2 = example_resonance_frequency + math.ceil(FSR_diff) * FSR
        print("There are two cavity resonances with similar distance to your frequency: " + str(resonance_1) + unit + "and " + str(resonance_2) + unit)
        print("The frequency offset is " + str(abs(frequency - resonance_1)) + unit + "and " + str(abs(frequency - resonance_2)) + unit)
    else:
        next_resonance = example_resonance_frequency + FSR * round(FSR_diff, 0)
        print("The next cavity resonance is at " + str(next_resonance) + unit)
        print("The frequency offset is " + str(abs(frequency - next_resonance)) + unit)



# Input/Output section:
ground_state = (5, 0, 0.5)
intermediate_state = (5, 1, 1.5)
rydberg_state = (47, 2, 1.5)


detuning_5P32 = (-113.2 * 1e6, - 83.8 * 1e6, - 20.4 * 1e6, 100.2 * 1e6)
detuning_to_5P32F4 = 100 * 1e6

FSR = 1521  # in MHz
example_resonance_frequency = 312365318  # in Mhz
frequency_57D52 = 312366106  # in MHz

resonance_list = cavity_resonance_list(FSR, example_resonance_frequency, 15)
print (resonance_list)

nearest_cavity_resonance(frequency_57D52, FSR, example_resonance_frequency, unit=" MHz ")

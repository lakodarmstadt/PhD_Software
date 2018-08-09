# Import section:
import sys
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


def nearest_cavity_resonance(wavelength, FSR, example_resonance):

    pass


# Input/Output section:
ground_state = (5, 0, 0.5)
intermediate_state = (5, 1, 1.5)
rydberg_state = (47, 2, 1.5)


detuning_5P32 = (-113.2 * 1e6, - 83.8 * 1e6, - 20.4 * 1e6, 100.2 * 1e6)
detuning_to_5P32F4 = 100 * 1e6



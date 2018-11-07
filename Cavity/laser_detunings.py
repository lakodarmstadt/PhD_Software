# Import section:
import sys
import math
sys.path.append('/home/lars/Dokumente/Lars_Kohfahl/Studium/PhD/PhD_Software')
from basic_definitions import *
from arc import *

atom = Rubidium85()
# Functions section:


def cavity_resonance_list(FSR, example_resonance_frequency, n):
    '''cavity_resonance_list(FSR, example_resonance_frequency, n)    function to calculate the n nearest resonances with respect to the example_resonance_frequency given the cavity FSR.'''

    resonance_list = [example_resonance_frequency + n * FSR for n in range(-n, n + 1)]
    return resonance_list


def nearest_cavity_resonance(frequency, FSR, example_resonance_frequency, unit=" Hz ", print_output=True):
    FSR_diff = (frequency - example_resonance_frequency) / FSR
    if abs(FSR_diff % 1) <= 0.55:
        resonance_1 = example_resonance_frequency + math.floor(FSR_diff) * FSR
        resonance_2 = example_resonance_frequency + math.ceil(FSR_diff) * FSR
        # print("There are two cavity resonances with similar distance to your frequency: " + str(resonance_1) + unit + "and " + str(resonance_2) + unit)
        # print("The frequency offset is " + str(abs(frequency - resonance_1)) + unit + "and " + str(abs(frequency - resonance_2)) + unit)
        # print("The frequency offset is " + str(resonance_1 - frequency) + unit + "and " + str(resonance_2 - frequency) + unit)
        frequency_offset = [resonance_1 - frequency, resonance_2 - frequency]
    else:
        next_resonance = example_resonance_frequency + FSR * round(FSR_diff, 0)
        # print("The next cavity resonance is at " + str(next_resonance) + unit)
        # print("The frequency offset is " + str(abs(frequency - next_resonance)) + unit)
        # print("The frequency offset is " + str(next_resonance - frequency) + unit)
        frequency_offset = [next_resonance - frequency]
    if print_output:
        print("The frequency offset is " + ' and '.join([str(i) for i in frequency_offset]) + ' MHz')
    return frequency_offset



# Input/Output section:
ground_state = (5, 0, 0.5)
intermediate_state = (5, 1, 1.5)
rydberg_state = (47, 2, 1.5)


detuning_5P32 = (-113.2 * 1e6, - 83.8 * 1e6, - 20.4 * 1e6, 100.2 * 1e6)
detuning_5S12 = (-1770.844 * 1e6, 1264.889 * 1e6)
detuning_to_5P32F4 = 100 * 1e6

FSR = 1496.923  # in MHz
example_resonance_frequency = 312365397  # in MHz; Example resonance frequency calculated from measurements June 18th 2018; corrected 07.11.2018 because of wrong frequency shift of cavity offsets (+-731Mhz bzw. +-788MHz); See Laserlevelschema_Rydberg_20181107.svg
# example_resonance_frequency = (384230406.373 * 1e6 + detuning_5P32[3] - detuning_5S12[1] - 4.301 * 1e6) / 1e6  # in MHz; Example Resonance at 780nm; 4.301MHz below Master which is 80Mhz above F'=4; measured at October 25th 2018


frequency_57D52 = (atom.getTransitionFrequency(5, 1, 1.5, 57, 2, 2.5) - detuning_5P32[3] - 406 * 1e6) / 1e6  # in MHz
# frequency_56D52 = (atom.getTransitionFrequency(5, 1, 1.5, 56, 2, 2.5) - detuning_5P32[3] - 406 * 1e6) / 1e6  # in MHz
# frequency_58D52 = (atom.getTransitionFrequency(5, 1, 1.5, 58, 2, 2.5) - detuning_5P32[3] - 406 * 1e6) / 1e6  # in MHz

# frequency_40D52 = (atom.getTransitionFrequency(5, 1, 1.5, 40, 2, 2.5) - detuning_5P32[3] - 406 * 1e6) / 1e6  # in MHz
# frequency_70D52 = (atom.getTransitionFrequency(5, 1, 1.5, 71, 2, 2.5) - detuning_5P32[3] - 406 * 1e6) / 1e6  # in MHz


# resonance_list = cavity_resonance_list(FSR, example_resonance_frequency, 15)
# print (resonance_list)

# nearest_cavity_resonance(frequency_57D52 * 0.5, FSR, example_resonance_frequency, unit=" MHz ")
# nearest_cavity_resonance(frequency_56D52 * 0.5, FSR, example_resonance_frequency, unit=" MHz ")
# nearest_cavity_resonance(frequency_58D52 * 0.5, FSR, example_resonance_frequency, unit=" MHz ")

# nearest_cavity_resonance(frequency_40D52 * 0.5, FSR, example_resonance_frequency, unit=" MHz ")
# nearest_cavity_resonance(frequency_70D52 * 0.5, FSR, example_resonance_frequency, unit=" MHz ")

offset_list = [[n, *nearest_cavity_resonance((atom.getTransitionFrequency(5, 1, 1.5, n, 2, 2.5) - detuning_5P32[3] - 406 * 1e6) / 1e6 * 0.5, FSR, example_resonance_frequency, unit=" MHz ", print_output=False)] for n in range(40, 81)]

print(offset_list)

offset_list_str = [[str(i) for i in item] for item in offset_list]

with open('offset_list_v1.txt', 'w') as f:
    for item in offset_list_str:
        f.write(' '.join(item)+'\n')

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import csv


# filename = '/home/lars/Dokumente/Lars_Kohfahl/Studium/PhD/Messungen/PDH_Abfallende_Flanke_Artefakt/verschieden Signale/Signal_Reflektion_ZAD.csv'


def keysight_header(filename):
    with open(filename, newline='') as f:
        reader = csv.reader(f)
        row1 = next(reader)  # gets the first line
        row2 = next(reader)
        header = [row1[0] + ' [' + row2[0] + ']', 'Channel ' + row1[1] + ' [' + row2[1] + ']', 'Channel ' + row1[2] + ' [' + row2[2] + ']']
        return header


def keysight_plotter(filename, title, save_filename):
    local_header = keysight_header(filename)
    data = pd.read_csv(filename, header=None, delimiter=',', skiprows=2)
    # print(data)
    print(local_header)
    # Note that using plt.subplots below is equivalent to using
    # fig = plt.figure() and then ax = fig.add_subplot(111)
    fig, ax1 = plt.subplots()
    ax1.plot(data[0], data[1], ':r')

    ax1.set_xlabel(local_header[0])
    ax1.set_ylabel(local_header[1], color='r')
    ax1.set_title(title)
    # ax1.grid()

    ax2 = ax1.twinx()
    ax2.plot(data[0], data[2], ':b')
    ax2.set_ylabel(local_header[2], color='b')
    fig.savefig(save_filename)
    plt.tight_layout()
    plt.show()


# keysight_plotter(filename)

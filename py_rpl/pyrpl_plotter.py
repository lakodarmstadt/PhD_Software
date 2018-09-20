# Important: Run this file in the pyrpl-environment you installed pyrpl.

import pyrpl
import pickle
import os
import numpy as np
import matplotlib.pyplot as plt


def load_data(filename):
    data_all = pickle.load(open(filename, "rb"))
    print(data_all[1])
    return data_all[1], data_all[2]


# filename1 = "/home/lars/pyrpl_user_dir/curve/1.dat"
# filename2 = "/home/lars/pyrpl_user_dir/curve/2.dat"


def pyrpl_plotter(filename1, filename2, title_name, save_filename):

    dict_1, data_1 = load_data(filename1)
    dict_2, data_2 = load_data(filename2)

    if np.shape(data_1) != np.shape(data_2):
        raise Exception('Input data has not equal dimension')

    if dict_1['xy_mode']:
        # Note that using plt.subplots below is equivalent to using
        # fig = plt.figure() and then ax = fig.add_subplot(111)
        fig, ax = plt.subplots()
        ax.plot(data_1[1], data_2[1])

        ax.set(xlabel=dict_1['input1'], ylabel=dict_2['input2'],
               title=title_name)
        ax.grid()

        fig.savefig(save_filename)
        plt.show()
    else:
        # Note that using plt.subplots below is equivalent to using
        # fig = plt.figure() and then ax = fig.add_subplot(111)
        fig, ax = plt.subplots()
        ax.plot(data_1[0], data_1[1])
        ax.plot(data_2[0], data_2[1])

        ax.set(xlabel='Time [s]', ylabel=dict_2['input2'],
               title=title_name)
        ax.grid()

        fig.savefig(save_filename)
        plt.show()

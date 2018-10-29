import numpy as np
import csv


def read_tectronix_rsa306(filename):

    raw_data = []

    with open(filename, 'rt') as csvfile:
        c = csv.reader(csvfile)

        trace_start_number = 0
        trace_found = False

        for row_num, row in enumerate(c):
            # print(row)
            if len(row) != 0 and row[0] == '[Traces]':
                trace_start_number = row_num
                trace_found = True

            if trace_found and row_num >= trace_start_number + 6:
                raw_data.append([float(row[0]), float(row[1])])

        return np.array(raw_data)

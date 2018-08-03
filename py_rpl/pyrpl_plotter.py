import pyrpl
import pickle
import os
import numpy as np
import matplotlib.pyplot as plt

curve_1 = pickle.load(open("/home/lars/pyrpl_user_dir/curve/2.dat", "rb"))
data_curve_1 = curve_1[2]


# Note that using plt.subplots below is equivalent to using
# fig = plt.figure() and then ax = fig.add_subplot(111)
fig, ax = plt.subplots()
ax.plot(data_curve_1[0], data_curve_1[1])

ax.set(xlabel='x', ylabel='y',
       title='About as simple as it gets, folks')
ax.grid()

# fig.savefig("test.png")
plt.show()

print(len(curve_1))


# curve_test = pyrpl.curvedb.CurveDB(name='test')
# curve_test.data = (0, 1)


# print(curve_test.params)

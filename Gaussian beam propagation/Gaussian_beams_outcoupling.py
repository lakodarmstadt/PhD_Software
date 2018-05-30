# Import area
import numpy as np
from sympy.physics.optics import rayleigh2waist, BeamParameter, FreeSpace, CurvedRefraction, FlatRefraction, ThinLens
import sympy as sp
from sympy.plotting import plot
from sympy.utilities.lambdify import lambdify
import operator
import matplotlib.pyplot as plt
from sympy import I, re, im

# Calculate beam propagation by multiplying the propagation matrices:


def calculateBeam(p, matrix_list):
    mat = reduce(operator.mul, matrix_list[::-1], 1)  # Multiply matrices
    print(mat)
    return mat * p


def calculateBeamInv(p, matrix_list):
    matrix_list_inv = [i.inv() for i in matrix_list]
    mat = reduce(operator.mul, matrix_list_inv[::], 1)  # Multiply matrices
    print(mat)
    return mat * p


def calculate_z(w, w_0, r_curv, wavelength):
    return -sp.sign(r_curv) * (np.pi * w_0**2 / wavelength) * ((w / w_0)**2 - 1.0)**0.5


# Calculate beam_parameters inside cavity:
def rayleigh_length(z, r_curv_at_z):
    return sp.sqrt(z * (r_curv_at_z - z))

# Define important constants


mm = 10**-3
um = 10**(-6)
nm = 10**(-9)
lambda_960 = 960 * nm
lambda_780 = 780 * nm
lambda_480 = 480 * nm
n_vac = 1
n_air = 1.000292  # For more exact value see Edlen1966

# Calculate the beam parameter representing the gaussian beam to start with:

# ####################Fiber and Laser parameters ###########################
# mode field diameter =2*waist
MFD = 3.4 * um
p_coupl = BeamParameter(lambda_480, 0, w=MFD / 2)

########################## Lens and geometry parameters ###############################
f_outcoupling = sp.symbols('f0', real=True)
# f_outcoupling = 7.5 * mm
l_outcoupling = f_outcoupling + 0.1 * mm
l_coll = 30 * 10**-3
l_EIT_cell = 120 * mm
f2 = 150 * 10**-3

######### List of optical components ###############
coupling_opt_list = []
coupling_opt_list.append(FreeSpace(l_outcoupling))
coupling_opt_list.append(ThinLens(f_outcoupling))
coupling_opt_list.append(FreeSpace(l_coll))
coupling_opt_list.append(ThinLens(f2))
coupling_opt_list.append(FreeSpace(l_EIT_cell))
# coupling_opt_list.append(ThinLens(t2))
# coupling_opt_list.append(FreeSpace(d1))


###### Calculate Beam Parameter p ##################
p_final = calculateBeam(p_coupl, coupling_opt_list)

# print(p_final.w)

#################### Further beam property calculations #######################
f_outcoupling_list = np.array([4.5 * mm, 6.24 * mm, 7.5 * mm, 8.2 * mm])
# l_coll_list = np.linspace(0.01, 0.2, 20)
# func_w_0 = lambdify(f_outcoupling, p_final.w_0, 'numpy')  # returns a numpy-ready function for w_0
func_w = lambdify(f_outcoupling, p_final.w, 'numpy')  # returns a numpy-ready function for w_0
func_z = lambdify(f_outcoupling, calculate_z(p_final.w, p_final.w_0, p_final.radius, lambda_780), 'numpy')  # returns a numpy-ready function for z
# func_r= lambdify(d0, p_final.radius,'numpy') # returns a numpy-ready function for radius of curvature
# w_0_list = func_w_0(f_outcoupling_list)
w_list = func_w(f_outcoupling_list)
z_list = func_z(f_outcoupling_list)
# r_list= func_r(d0_list)

print(w_list)
print(z_list)
# print(w_0_list)

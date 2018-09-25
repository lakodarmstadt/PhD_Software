import sys
import scipy.integrate as integrate
sys.path.append('/home/lars/Dokumente/Lars_Kohfahl/Studium/PhD/PhD_Software/Calculate waists')
from waist_fitting import gaussian_2D
import numpy as np


def fit_gaussian_to_square_aperture(height, center_x, center_y, waist_x, waist_y, x_lower_bound, x_upper_bound, y_lower_bound, y_upper_bound):
    ''' This function prints and returns the relative power transmitted through a rectangular aperture'''
    result, error = integrate.dblquad(gaussian_2D(height, center_x, center_y, waist_x, waist_y, 0), x_lower_bound, x_upper_bound, y_lower_bound, y_upper_bound)
    total_power = (np.pi * height * ((waist_x**2 + waist_y**2) / 2) / 2)
    # Note: elliptical beams not calculated correctly?
    print('The Transmission through the aperture is ' + str(result * 100 / total_power) + '%.')
    # return


x_length = 9.6e-3
y_length = 9.72e-3
x_displacement = 1e-3
y_displacement = 1e-3

x_lower_bound = -x_length / 2 + x_displacement
x_upper_bound = x_length / 2 + x_displacement
y_lower_bound = -y_length / 2 + y_displacement
y_upper_bound = y_length / 2 + y_displacement

# x_lower_bound = -5e-1
# x_upper_bound = 5e-1
# y_lower_bound = -5e-1
# y_upper_bound = 5e-1

height = 1
center_x = 0
center_y = 0
waist_x = 2.7e-3
waist_y = 2.7e-3
offset = 0


fit_gaussian_to_square_aperture(height, center_x, center_y, waist_x, waist_y, x_lower_bound, x_upper_bound, y_lower_bound, y_upper_bound)

# gaussian_2D(height, center_x, center_y, waist_x, waist_y,offset)

import numpy as np
from scipy import misc
from scipy.optimize import minimize,fsolve
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

def gaussian_1D(height, center, width, offset):
    width=float(width) #width is defined as 1/e^2 of the intensity
    return lambda x: height*np.exp(-2*((center-x)/width)**2)+offset

def gaussian_2D(height, center_x, center_y, width_x, width_y,offset):
    """Returns a gaussian function with the given parameters"""
    width_x = float(width_x)
    width_y = float(width_y)
    return lambda x,y: height*np.exp(-2*(((center_x-x)/width_x)**2+((center_y-y)/width_y)**2))+offset
    
def Power_gaussian_2D_symmetric(height, radius, width):
    """Returns a gaussian function with the given parameters"""
    width = float(width)
    return height*(1-np.exp(-2*(radius**2/width**2)))
    
print(Power_gaussian_2D_symmetric(321.2,3.05,3.21))

fit = lambda x: Power_gaussian_2D_symmetric(321.2,3.05,x) - 268.3
res = fsolve(fit,3.05)
print(res)
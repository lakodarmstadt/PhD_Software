import numpy as np
from scipy import misc
from scipy import optimize
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import os

def gaussian_1D(height, center, waist, offset):
    waist=float(waist) #waist is defined as 1/e^2 of the intensity
    return lambda x: height*np.exp(-2*((center-x)/waist)**2)+offset

def gaussian_2D(height, center_x, center_y, waist_x, waist_y,offset):
    """Returns a gaussian function with the given parameters"""
    waist_x = float(waist_x)
    waist_y = float(waist_y)
    return lambda x,y: height*np.exp(-2*(((center_x-x)/waist_x)**2+((center_y-y)/waist_y)**2))+offset

def data_1D_av(data,i,j):
    data_i=np.sum(data,axis=0)
    data_j=np.sum(data,axis=1)
    return data_i,data_j

def moments_1D(data):
    """Returns (height, x, y, waist_x, waist_y)
    the gaussian parameters of a 1D distribution by calculating its
    moments """
    total = data.sum()
    I = np.indices(data.shape)
    i = (I*data).sum()/total
    waist = np.sqrt(np.abs((np.arange(data.size)-i)**2*data).sum()/data.sum())
    height = data.max()
    offset=data.min()
    return height,i,waist,offset


def moments_2D(data):
    """Returns (height, x, y, waist_x, waist_y)
    the gaussian parameters of a 2D distribution by calculating its
    moments """
    total = data.sum()
    I, J = np.indices(data.shape)
    #Find mass centre of intensity distribution
    i = (I*data).sum()/total
    j = (J*data).sum()/total
    col = data[:, int(j)]
    waist_i = np.sqrt(np.abs((np.arange(col.size)-i)**2*col).sum()/col.sum())
    row = data[int(i), :]
    waist_j = np.sqrt(np.abs((np.arange(row.size)-j)**2*row).sum()/row.sum())
    height = data.max()
    offset=data.min()
    return height, i, j, waist_i, waist_j,offset

def fitgaussian_1D(data):
    """Returns (height, i, j, waist_i, waist_j)
    the gaussian parameters of a 1D distribution found by a fit"""
    params = moments_1D(data)
    print(params)

    #gaussian_2D(*p) is a function taking two arguments, which are in the case used here two 2D matrices created by np.indices.
    # The error function is then a function depending on the parameters p which gets least if gaussian_2D best fits data.
    errorfunction = lambda p: np.ravel(gaussian_1D(*p)(*np.indices(data.shape))-data)

    p, pcov, infodict, errmsg, success = optimize.leastsq(errorfunction, params, full_output=1)
    #print('Gaussian_2D:')
    #print(gaussian_2D(*p))
    #print('Product:')
    #print((*np.indices(data.shape)))
    #print(gaussian_2D(*p)(*np.indices(data.shape)))
    #print('Data:')
    #print(data)

    return p, pcov, success

def fitgaussian_2D(data):
    """Returns (height, i, j, waist_i, waist_j)
    the gaussian parameters of a 2D distribution found by a fit"""
    params = moments_2D(data)
    print(params)

    #gaussian_2D(*p) is a function taking two arguments, which are in the case used here two 2D matrices created by np.indices.
    # The error function is then a function depending on the parameters p which gets least if gaussian_2D best fits data.
    errorfunction = lambda p: np.ravel(gaussian_2D(*p)(*np.indices(data.shape))-data)

    p, pcov, infodict, errmsg, success = optimize.leastsq(errorfunction, params, full_output=1)
    #print('Gaussian_2D:')
    #print(gaussian_2D(*p))
    #print('Product:')
    #print((*np.indices(data.shape)))
    #print(gaussian_2D(*p)(*np.indices(data.shape)))
    #print('Data:')
    #print(data)

    return p, pcov, success



def fit_gaussian_2D_to_image(filename, pixelsize_x=3.75, pixelsize_y=3.75, sliceing=None):
    data = np.array(misc.imread(filename))
    if sliceing is not None:
        data = data[sliceing[0][0]:sliceing[0][1], sliceing[1][0]:sliceing[1][1]]

    fig = plt.figure(figsize=(5,4),tight_layout=True)
    #plt.matshow(data, cmap=plt.cm.gist_earth_r)
    plt.matshow(data, cmap='gray')


    params, pcov, success = fitgaussian_2D(data)
    fit = gaussian_2D(*params)

    plt.contour(fit(*np.indices(data.shape)), cmap=plt.cm.copper)
    ax = plt.gca()
    ax.xaxis.set_tick_params(labeltop='off', labelbottom='on')
    (height, i, j, waist_i, waist_j,offset) = params
    print('2D params are:')
    print(params)
    print(np.sqrt(np.diag(pcov)))
    print(success)
    plt.text(0.95, 0.05, """
    waist_x : %.1fum
    waist_y : %.1fum""" %(waist_j*pixelsize_x, waist_i*pixelsize_y),
            fontsize=12, horizontalalignment='right', color= 'r',
            verticalalignment='bottom', transform=ax.transAxes)
    plt.text(0.7, 0.9, filename,
            fontsize=12, horizontalalignment='right', color= 'r',
            verticalalignment='bottom', transform=ax.transAxes)
    ax.set_xlabel('x-axis camera')
    ax.set_ylabel('y-axis camera')
    #fig.tight_layout()
    plt.savefig(filename + '.pdf', bbox_inches='tight', format='pdf')

def fit_gaussian_1D_to_image(filename, pixelsize_x=3.75, pixelsize_y=3.75, lin=True):
    # Data needs to be transposed to have the pictures x-axis as first index in the array: (x,y)
    data = np.array(misc.imread(filename)).T

    gs = gridspec.GridSpec(3,2,height_ratios = [2,2,1])

    fig = plt.figure(figsize=(10,10),tight_layout=True)

    ax1 = plt.subplot(gs[0:2, :]) #row 0, span all columns
    ax1.matshow(data, cmap=plt.cm.gist_earth_r)

    params, pcov, success = fitgaussian_2D(data)
    fit = gaussian_2D(*params)

    ax1.contour(fit(*np.indices(data.shape)), cmap=plt.cm.copper)
    ax1.xaxis.set_tick_params(labeltop='off', labelbottom='on')
    ax1.set_xlabel('y-axis camera')
    ax1.set_ylabel('x-axis camera')
    #axtext = ax1.gca()
    (height, i, j, waist_i, waist_j,offset) = params
    print('2D params are:')
    print(params)
    print(np.sqrt(np.diag(pcov)))
    print(success)
    ax1.text(0.95, 0.05, """
    waist_x : %.1fum
    waist_y : %.1fum""" %(waist_j*pixelsize_x, waist_i*pixelsize_y),
            fontsize=16, horizontalalignment='right', color= 'r',
            verticalalignment='bottom', transform=ax1.transAxes)
    ax1.text(0.5, 0.9, filename,
            fontsize=16, horizontalalignment='right', color= 'r',
            verticalalignment='bottom', transform=ax1.transAxes)
    if lin==True:
        data_i,data_j=data[:,int(np.round(y,0))],data[int(np.round(x,0)),:]
        filename+='_1D_lin_'+'.pdf'
    else:
        data_i,data_j=data_1D_av(data,i,j)
        filename+='_1D_avg_'+'.pdf'


    params_i, pcov_i, success_i=fitgaussian_1D(data_i)
    params_j, pcov_j, success_j=fitgaussian_1D(data_j)
    print('1D_x params are:')
    print(params_j)
    print('1D_y params are:')
    print(params_i)
    waist_i_1D,waist_j_1D=params_i[2],params_j[2]

    # Be aware that i is the row-index specifying the vertical (so the y-) axis of the image. Correspondingly j is the index for the x-axis.
    fit_i=gaussian_1D(*params_i)
    fit_j=gaussian_1D(*params_j)

    ax2 = plt.subplot(gs[2, 0]) # row 1, col 0
    ax2.plot(data_i,'ro')
    ax2.plot(fit_i(*np.indices(data_i.shape)))
    ax2.text(0.95, 0.05, """
    waist_y : %.1fum""" %(waist_i_1D*pixelsize_y),
            fontsize=16, horizontalalignment='right',
            verticalalignment='bottom', transform=ax2.transAxes)

    ax3 = plt.subplot(gs[2, 1]) # row 1, col 1
    ax3.plot(data_j,'ro')
    ax3.plot(fit_j(*np.indices(data_j.shape)))
    ax3.text(0.95, 0.05, """
    waist_x : %.1fum""" %(waist_j_1D*pixelsize_x),
            fontsize=16, horizontalalignment='right',
            verticalalignment='bottom', transform=ax3.transAxes)

    plt.savefig(filename, format='pdf')



#dir_path = os.path.dirname(os.path.realpath(__file__))
#print(dir_path)
#Create a list of all picture files:
#files = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith('.pgm')] #os.path.isfile(f) and  files.endswith('.pgm')
#print(files)
#for f in files:
#    fit_gaussian_2D_to_image(f)




#fit_gaussian_1D_to_image('2018_03_07/dist300mm.pgm')
#fit_gaussian_1D_to_image('2018_03_07/dist300mm_off_axis.pgm')
#fit_gaussian_1D_to_image('2018_03_06/dist300mm.pgm')
#fit_gaussian_1D_to_image('2018_03_06/dist450mm.pgm')
#fit_gaussian_1D_to_image('2018_03_06/dist690mm.pgm')
#fit_gaussian_2D_to_image('/home/lars/Dokumente/Lars_Kohfahl/Studium/PhD//Messungen/Fibercollimator_F810APC-780/2018_03_14/backup_test.pgm')
#fit_gaussian_2D_to_image('/home/lars/Dokumente/Lars_Kohfahl/Studium/PhD/Lehre/FP/Messungen_LK/2018_04_05/Ladephase/Ladephase0009.bmp')

#plt.show()
#plt.savefig('fitresults_2018_03_07.pdf')

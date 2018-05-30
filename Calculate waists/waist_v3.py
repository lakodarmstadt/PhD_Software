import numpy as np
from scipy import misc
from scipy import optimize
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import os

def gaussian_1D(height, center, width, offset):
    width=float(width) #width is defined as 1/e^2 of the intensity
    return lambda x: height*np.exp(-2*((center-x)/width)**2)+offset

def gaussian_2D(height, center_x, center_y, width_x, width_y,offset):
    """Returns a gaussian function with the given parameters"""
    width_x = float(width_x)
    width_y = float(width_y)
    return lambda x,y: height*np.exp(-2*(((center_x-x)/width_x)**2+((center_y-y)/width_y)**2))+offset

def data_1D_av(data,x,y):
    data_x=np.sum(data,axis=0)
    data_y=np.sum(data,axis=1)
    return data_x,data_y
   
def moments_1D(data):
    """Returns (height, x, y, width_x, width_y)
    the gaussian parameters of a 1D distribution by calculating its
    moments """
    total=data.sum()
    X=np.indices(data.shape)
    x = (X*data).sum()/total
    width = np.sqrt(np.abs((np.arange(data.size)-x)**2*data).sum()/data.sum())
    height = data.max()
    offset=data.min()
    return height,x,width,offset
    

def moments_2D(data):
    """Returns (height, x, y, width_x, width_y)
    the gaussian parameters of a 2D distribution by calculating its
    moments """
    total = data.sum()
    X, Y = np.indices(data.shape)
    #Find mass centre of intensity distribution
    x = (X*data).sum()/total
    y = (Y*data).sum()/total
    col = data[:, int(y)]
    width_x = np.sqrt(np.abs((np.arange(col.size)-x)**2*col).sum()/col.sum())
    row = data[int(x), :]
    width_y = np.sqrt(np.abs((np.arange(row.size)-y)**2*row).sum()/row.sum())
    height = data.max()
    offset=data.min()
    return height, x, y, width_x, width_y,offset

def fitgaussian_1D(data):
    """Returns (height, x, y, width_x, width_y)
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
    """Returns (height, x, y, width_x, width_y)
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
    (height, x, y, width_x, width_y,offset) = params
    print('2D params are:')
    print(params)
    print(np.sqrt(np.diag(pcov)))
    print(success)
    plt.text(0.95, 0.05, """
    width_x : %.1fum
    width_y : %.1fum""" %(width_x*pixelsize_x, width_y*pixelsize_y),
            fontsize=12, horizontalalignment='right',
            verticalalignment='bottom', transform=ax.transAxes)
    plt.text(0.7, 0.9, filename,
            fontsize=12, horizontalalignment='right',
            verticalalignment='bottom', transform=ax.transAxes)
    ax.set_xlabel('y-axis camera')
    ax.set_ylabel('x-axis camera')
    #fig.tight_layout()
    plt.savefig(filename+'.pdf', bbox_inches='tight',format='pdf')

def fit_gaussian_1D_to_image(filename, pixelsize_x=3.75, pixelsize_y=3.75, lin=True):
    data = np.array(misc.imread(filename))

    gs = gridspec.GridSpec(3,2,height_ratios=[2,2,1])
    
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
    (height, x, y, width_x, width_y,offset) = params
    print('2D params are:')    
    print(params)
    print(np.sqrt(np.diag(pcov)))
    print(success)
    ax1.text(0.95, 0.05, """
    waist_x : %.1fum
    waist_y : %.1fum""" %(width_x*pixelsize_x, width_y*pixelsize_y),
            fontsize=16, horizontalalignment='right',
            verticalalignment='bottom', transform=ax1.transAxes)
    ax1.text(0.5, 0.9, filename,
            fontsize=16, horizontalalignment='right',
            verticalalignment='bottom', transform=ax1.transAxes)
    if lin==True:
        data_x,data_y=data[:,int(np.round(y,0))],data[int(np.round(x,0)),:]
        filename+='_1D_lin_'+'.pdf'
    else:
        data_x,data_y=data_1D_av(data,x,y)
        filename+='_1D_avg_'+'.pdf'
    
    
    params_x, pcov_x, success_x=fitgaussian_1D(data_x)
    params_y, pcov_y, success_y=fitgaussian_1D(data_y)
    print('1D_x params are:')
    print(params_x)
    print('1D_y params are:')
    print(params_y)
    width_x_1D,width_y_1D=params_x[2],params_y[2]
    
    fit_x=gaussian_1D(*params_x)
    fit_y=gaussian_1D(*params_y)
    
    ax2 = plt.subplot(gs[2, 0]) # row 1, col 0
    ax2.plot(data_x,'ro')    
    ax2.plot(fit_x(*np.indices(data_x.shape)))
    ax2.text(0.95, 0.05, """
    waist_x : %.1fum""" %(width_x_1D*pixelsize_x),
            fontsize=16, horizontalalignment='right',
            verticalalignment='bottom', transform=ax2.transAxes)

    ax3 = plt.subplot(gs[2, 1]) # row 1, col 1
    ax3.plot(data_y,'ro')
    ax3.plot(fit_y(*np.indices(data_y.shape)))
    ax3.text(0.95, 0.05, """
    waist_y : %.1fum""" %(width_y_1D*pixelsize_y),
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
fit_gaussian_2D_to_image('2018_03_14/backup_test.pgm')


#plt.show()
#plt.savefig('fitresults_2018_03_07.pdf')

from sympy.physics.optics import RayTransferMatrix, ThinLens, FreeSpace, BeamParameter
from sympy import Symbol, Matrix, symbols, solve
from sympy.physics.optics import BeamParameter, GeometricRay
import numpy as np
import operator
wavelen = 796e-9
z = 0
w = 2.65e-6
w_aom = 2e-3
w_falle = 1.5e-6
d_aom = 7.5e-3
deflection_angle = 0.046
array_pitch = 10e-6

def collimate(collimation_lense, f_coll=None):
    if collimation_lenses == 1:
        f_colimation = f_coll[0] if f_coll else np.pi * w_aom * p.w / wavelen
        print('focalength collimation fiber: {}mm'.format(f_colimation*1e3))
        fs = FreeSpace(f_colimation)
        lens = ThinLens(f_colimation)
        mat = lens*fs
    elif collimation_lenses == 2:
        f_colimation = np.pi * w_aom * p.w / wavelen
        print('total focalength collimation: {}mm'.format(f_colimation*1e3))

        f1 = f_coll[0]
        f2 = f_coll[1]
        d = Symbol('d')
        fges = f_colimation

        dist = solve(1/f1+1/f2-d/(f1*f2)-1/fges, d)[0]

        b_eff=fges-dist*(fges/f2)
        fs = FreeSpace(fges-dist*(fges/f2))
        print('distance fibre -> first collimation lens: {}mm'.format(b_eff*1e3))
        lens = ThinLens(f_coll[0])
        mat = lens*fs
        print('focalength first collimation lens: {}mm'.format(f_coll[0]*1e3))

        print('collimation lens distance: {}mm'.format(dist*1e3))
        fs = FreeSpace(dist)
        lens1 = ThinLens(f_coll[1])
        mat = lens1*fs*mat
        print('focalength second collimation lens: {}mm'.format(f_coll[1]*1e3))

    elif collimation_lenses == 3:
        fs = FreeSpace(f_coll[0])
        lens = ThinLens(f_coll[0])
        mat = lens*fs
        print('focalength collimation fiber: {}mm'.format(f_coll[0]*1e3))

        lens1 = ThinLens(f_coll[1])
        fs = FreeSpace(f_coll[1])
        mat = fs*lens1*mat
        print('focalength first collimation magnification lens: {}mm'.format(f_coll[1]*1e3))

        fs = FreeSpace(f_coll[2])
        lens2 = ThinLens(f_coll[2])
        mat = lens2*fs*mat
        print('focalength second collimation magnification lens: {}mm'.format(f_coll[2]*1e3))
    print('')
    return mat

def magnify(f1_imaging, f2_imaging):
    imaging_lens1 = ThinLens(f1_imaging)
    fs1 = FreeSpace(f1_imaging)
    print('focalength first imaging lens: {}mm'.format(f1_imaging*1e3))

    fs2 = FreeSpace(f2_imaging)
    imaging_lens2 = ThinLens(f2_imaging)
    print('focalength second imaging lens: {}mm'.format(f2_imaging*1e3))

    return imaging_lens2*fs2*fs1*imaging_lens1

def calcualteBeam(wavelen, elements, z=0, w=w):
    p = BeamParameter(wavelen, z, w=w)
    mat = reduce(operator.mul, elements[::-1], 1)  # Multiply matrices
    return mat * p

def calcualteGeoBeam(wavelen, elements, z=0, w=w):
    p = BeamParameter(wavelen, z, w=w)
    p = GeometricRay(w, p.divergence)
    mat = reduce(operator.mul, elements[::-1], 1)  # Multiply matrices
    return mat * p

# 1 Lense Collimation
# collimation_lenses = 1
# f_coll = [183e-3]

# 2 Lense Collimation
# collimation_lenses = 2
# f_coll = [11e-3, 100e-3]

# 3 Lense Collimation
collimation_lenses = 3
f_coll = [11e-3, 50e-3, 100e-3]
#f_coll = [8e-3, 50e-3, 125e-3]

magnification_imaging = 4#1893350476839
f1_imaging = 100e-3 # -50e3
f2_imaging = f1_imaging * magnification_imaging # 150e-3

f_bonner_monster = 35.5e-3

elements = []
p = BeamParameter(wavelen, z, w=w)
elements.append(collimate(collimation_lenses, f_coll))
elements.append(FreeSpace(40e-2))
p = calcualteBeam(wavelen, elements, z=0, w=w)
print('Collimated Waist: {}mm'.format(p.w.evalf()*1e3))
print('Divergence: {}'.format(p.divergence.evalf()))
w_aom = float(p.w)
trasmitted = 1-np.exp(-(2*(d_aom/2.0)**2)/(w_aom**2))
print("AOM Loss: {}%".format((1-trasmitted)*100))

print('')
elements.append(magnify(f1_imaging, f2_imaging))
elements.append(FreeSpace(0.8))
p = calcualteBeam(wavelen, elements, z=0, w=w)
print('After Magnification Waist: {}mm'.format(p.w.evalf()*1e3))
# bonner monster
bonner_monster = FreeSpace(f_bonner_monster)*ThinLens(f_bonner_monster)
elements.append(bonner_monster)
p = calcualteBeam(wavelen, elements, z=0, w=w)
print('Trap Waist: {}um'.format(p.w.evalf()*1e6*np.sqrt(2)))
traps = np.pi * w_aom * float(p.w)/wavelen*np.tan(deflection_angle) / array_pitch
print("Fallen: {}".format(traps))

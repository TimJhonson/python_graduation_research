import pandas as pd  
import matplotlib.pyplot as plt 
from scipy.interpolate import interp1d
import glob
import numpy as np
from scipy.interpolate import interp1d
import PIL.Image as Image
import os



##### LAO
LAOdata = pd.read_csv('C:/Users/Tim/Desktop/SUM/201230_001_LAO#2020-11-19-(10)_CoL23_T33K.dat',encoding='utf-8',delimiter="\t" )
LAOdata = LAOdata[2690:8650]
LAO_LH = LAOdata["LH"]
LAO_LV = LAOdata["LV"] 
LAOxmld = LAOdata["LH"]+2*LAOdata["LV"] 
LAO_experiment = LAO_LH - LAO_LV - 0.3
LAOdata["Energy(eV)"] = LAOdata["Energy(eV)"] - 783.7



LS = pd.read_csv('C:/Users/Tim/Desktop/理論數據/Theory/LS/Co_210324_005_722_LS_aDeg0.0_aDt2g0.0' + '_XAS.dat', sep="\s+",    encoding='utf-8',skiprows=6,engine='python',header=None ) 
        
    
  
    

    
### LS
LS = LS[20:2000]

##### LS polar x
chLSx = 0.16
LSx_x = (LS[0]+chLSx).values
LSx_y = LS[2].values
#####  LS polar y
LSy_x = LSx_x
LSy_y = (LS[4]).values
#####  LS polar z
LSz_x = LSx_x
LSz_y = (LS[6]).values
LSxyz = -1*(LSx_y + LSy_y + LSz_y)/3
 
###設arctan,使用numpy的array
x1 = np.arange(-10, -5, 0.01, float)
x2 = np.arange(-5, -2, 0.01, float)
x3 = np.arange(-2, 9.5, 0.01, float)
x4 = np.arange(9.5, 11.5, 0.01, float)
x5 = np.arange(11.5, 20, 0.01, float)
arct2 = 0.006*np.arctan(8*(x2-(-3))) 
arct1 = np.full_like(x1,np.min(arct2))
arct3 = np.full_like(x3,np.max(arct2))
arct4 = 0.004*np.arctan(8*(x4-10.5)) +0.014
arct5 = np.full_like(x5,np.max(arct4))
arct = np.hstack([arct1,arct2,arct3,arct4,arct5])
x = np.hstack([x1,x2,x3,x4,x5]) 
### arct,LS,內插後相加,使用numpy的array
f = interp1d(x,arct,fill_value='extrapolate')
#以LS的x軸為基準
arct = f(LSx_x)
LSxyz = LSxyz + arct 
 
LSxyz = 1.15*LSxyz 
 

# LSglf1 =  1.650 
# LSglf2 =  0.3420
# LSglf3 =  0.060
# LSglf5 =  0.11250
# LSglf9 =  0.020
# LSglfelv = 0.0
# LSglftwf = 0.1150
# glf14th = round((i-1)*0.06,2)
# LSGLx = [-0.2000000E+02+chLSx,       
#          -0.5800000E+01+chLSx,            
#          -0.4200000E+01+chLSx,       
#          -0.4100000E+01+chLSx,       
#          -0.3400000E+01+chLSx,  
#           0.0000000E+00-LSglf1+chLSx,   
# 	      0.3000000E+01+chLSx,       
# 	      0.8000000E+01+chLSx,       
# 	      0.1030000E+02+chLSx,       
# 	      0.1130000E+02+chLSx,       
# 	      0.150000E+02+chLSx,        
#         ]

# LSGLy = [
#         0.1000000E+00+LSglf9+LSglftwf,
#         0.1000000E+00+LSglf9+LSglftwf,
#         0.8*0.1130000E+01+LSglf9,
#         0.8*0.1130000E+01+LSglf9,
#         0.8*0.1130000E+01+LSglf9,
#         0.8*0.1130000E+01-0.2280+LSglf2,
#         0.8*0.1130000E+01-0.2280+LSglf2,
#         0.6000000E+00,            
#         0.6000000E+00,
#         0.6000000E+00+LSglf3+LSglf5+LSglfelv+glf14th,
#         0.6000000E+00+LSglf3+LSglf5+LSglfelv+glf14th,
#     ]
# HSgl2 =  0.150 
# HSgl3 =  0.1150
# HSgl5 =  2.50
# HSGLx = [
#         -0.2000000E+02+chHSx,
#         -0.7600000E+01+chHSx, 
#         -0.7200000E+01+chHSx, 
#         -0.4900000E+01+chHSx, 
#         -0.4100000E+01+chHSx, 
#         -0.3200000E+01+chHSx, 
#         -0.2400000E+01+chHSx, 
#     	 0.0000000E+00+chHSx, 
#     	 0.3000000E+01+chHSx, 
#     	 0.8000000E+01+chHSx, 
#     	 0.1030000E+02+chHSx, 
#     	 0.1040000E+02+chHSx+HSgl5, 
#         ]   
# HSGLy = [
#        0.7500000E+00+HSgl2+HSgl3,
#        0.7500000E+00+HSgl2+HSgl3,
#        0.7500000E+00+HSgl2+HSgl3,
#        0.7500000E+00+HSgl2+HSgl3,
#        0.1130000E+01,
#        0.1130000E+01,
#        0.1130000E+01,
#        0.1350000E+01,
#        0.1350000E+01,
#        0.8500000E+00,
#        0.8500000E+00,
#        0.1500000E+01,
#     ]

# LSGLy = np.multiply(LSGLy, 0.3)
# HSGLy = np.multiply(HSGLy, 0.3)

plt.plot(LAOdata["Energy(eV)"],LAOxmld-0.3,label='experiment of LAO',color = 'b')


plt.plot(LSx_x,LSxyz,label= 'LSDq0.62',color='r')
 
 
plt.rc('legend',fontsize=6)
plt.xlim(-10,20)
plt.legend()
plt.grid(True)
plt.title( 'LAO  experiment vs theory 100%'   )
plt.savefig('LAO_XAS.png')
plt.show()
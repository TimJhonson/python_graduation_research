from STO_XAS import STO_experiment
from numpy.core.shape_base import block
import pandas as pd  
import matplotlib.pyplot as plt 
from scipy.interpolate import interp1d
import glob
import numpy as np
from scipy.interpolate import interp1d
import PIL.Image as Image
import os
import cv2

### STO
STOdata = pd.read_csv('C:/Users/Tim/Desktop/實驗_XMCD/210324_001_STO#2020-10-26-(25)-No1_XMCD_CoL23_T025K_02_01.dat',encoding='utf-8',delimiter="\t" )
STOdata = STOdata[2690:8650]
STOxmld = STOdata["LH"]+2*STOdata["LV"] #+0.3
STOdata["Energy(eV)"] = STOdata["Energy(eV)"] - 780.4
STO_experiment = STOdata["LH"] - STOdata["LV"] - 0.8
     
LS = pd.read_csv('C:/Users/Tim/Desktop/理論數據/Theory/LS/Co_210324_005_722_LS_aDeg-0.150' + '_aDt2g-0.050' +'_XAS.dat', sep="\s+",    encoding='utf-8',skiprows=6,engine='python',header=None ) 

              
HS = pd.read_csv('C:/Users/Tim/Desktop/理論數據/Theory/HS/Co_210325_004_HS_724_aDeg-0.150' + '_aDt2g-0.050' + '_XAS.dat', sep="\s+",    encoding='utf-8',skiprows=6,engine='python',header=None ) 


#####LS
LS = LS[20:2000]

chLSx = 0.16
#####  LS polar x

LSx_x = (LS[0]+chLSx).values

LSx_y = LS[2].values

#####  LS polar y

LSy_x = LSx_x
LSy_y = (LS[4]).values
     
LSy_y = -1*LSy_y-0.0054

#####  LS polar z

LSz_x = LSx_x

LSz_y = (LS[6]).values
LSz_y = -1*LSz_y-0.0054
#####HS
HS = HS[20:2000]

chHSx = -0.23
#####  HS polar x

HSx_x = (HS[0]+chHSx).values

HSx_y = HS[2].values

#####  HS polar y

HSy_x = HSx_x
    
HSy_y = HS[4].values

HSy_y = -1*HSy_y-0.0044
#####  HS polar Z

HSz_x = HSx_x

HSz_y = HS[6].values

HSz_y = -1*HSz_y-0.0044

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

arct = arct + 0.0088

##LAO,LS的xmld,內插後相加,使用numpy的array
f = interp1d(x,arct,fill_value='extrapolate')
#以LS的x軸為基準
arct = f(LSx_x)
LSy_y = LSy_y + arct 
LSz_y = LSz_y + arct 
arct = f(HSx_x)
HSy_y = HSy_y + arct
HSz_y = HSz_y + arct

#plt.plot(LSx_x,LSy_y,color='orange')
#LV
f = interp1d(HSx_x,HSy_y,fill_value='extrapolate')
HSy_y = f(LSx_x)
#plt.plot(LSx_x,HSy_y,color='orange')
STOy = 0.5*(0.76*LSy_y + 0.24*HSy_y)-0.07 #-1.05+(i-1)*0.35
#plt.plot(LSx_x,STOy,color='b')
#LH
f = interp1d(HSx_x,HSz_y,fill_value='extrapolate')
HSz_y = f(LSx_x)
STOz = 0.5*(0.76*LSz_y + 0.24*HSz_y)-0.07 #-1.05+(i-1)*0.35

STO_theory = STOz - STOy - 0.14

plt.plot(STOdata["Energy(eV)"],STOdata["LV"],label='experiment LV',color='b')
plt.plot(STOdata["Energy(eV)"],STOdata["LH"],label='experiment LH',color='r')
plt.plot(LSx_x,STOy,label= 'theory LV of HS Deg'+ '-0.15' + ' Dt2g'+ '-0.05',color='b')
plt.plot(LSx_x,STOz,label= 'theory LH of HS Deg'+ '-0.15' + ' Dt2g'+ '-0.05',color='r')
plt.plot(STOdata["Energy(eV)"],STO_experiment,label='experiment of LH-LV',color='black')
plt.plot(LSx_x,STO_theory,label = 'theory of LH-LV',color='orange')
plt.plot(STOdata["Energy(eV)"],(STOdata["LV"]+STOdata["LH"])/2,color='g')
   
plt.rc('legend',fontsize=5.5)
plt.legend()    
plt.grid(True)
 
plt.title( 'try 76%LS+24%HS'  )
plt.savefig('try.png')
plt.show()

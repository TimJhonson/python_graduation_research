import pandas as pd  
import matplotlib.pyplot as plt 
from scipy.interpolate import interp1d
import glob
import numpy as np
from scipy.interpolate import interp1d
import PIL.Image as Image
import os


###別條線做出的數據
LAOdata = pd.read_csv('C:/Users/Tim/Desktop/SUM/201230_001_LAO#2020-11-19-(10)_CoL23_T33K.dat',encoding='utf-8',delimiter="\t" )
LAOdata = LAOdata[2690:8650]
LAO_LH = LAOdata["LH"]
LAO_LV = LAOdata["LV"] 
LAO_experiment = LAO_LH - LAO_LV - 0.14
LAOdata["Energy(eV)"] = LAOdata["Energy(eV)"] - 783.85



LS = pd.read_csv('C:/Users/Tim/Desktop/理論數據/Theory/LS/Co_210324_005_722_LS_aDeg0.0' + '_aDt2g0.0' +'_XAS.dat', sep="\s+",    encoding='utf-8',skiprows=6,engine='python',header=None ) 

   



LS = LS[20:2000]

#####  LS polar x

LSx_x = (LS[0]).values

LSx_y = LS[2].values

#####  LS polar y

LSy_x = (LS[0]).values
LSy_y = (LS[4]).values

LSy_y = -1*LSy_y - 0.0041 #- 0.1
#####  LS polar z

LSz_x = LSx_x

LSz_y = (LS[6]).values 
LSz_y = -1*LSz_y - 0.0041 #- 0.1
LAO_theory = LSz_y - LSy_y -0.14

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

LSy_y = 0.38*LSy_y-0.07
LSz_y = 0.38*LSz_y-0.07


plt.plot(LAOdata["Energy(eV)"],LAO_LV,label='experiment LV',color='b')
plt.plot(LAOdata["Energy(eV)"],LAO_LH,label='experiment LH',color='r')
plt.plot(LSx_x,LSy_y,label= 'theory LV ',color='b')
plt.plot(LSx_x,LSz_y,label= 'theory LH ',color='r')
plt.plot(LAOdata["Energy(eV)"],LAO_experiment,label='experiment of LH-LV',color='black')
plt.plot(LSx_x,LAO_theory,label = 'theory of LH-LV',color='orange')
plt.rc('legend',fontsize=5.5)
plt.legend()    
plt.grid(True)

plt.title( 'LAO XMLD 100%LS')
plt.savefig('LAO_XMLD.png')
plt.show()
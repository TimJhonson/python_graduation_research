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
STOdata = STOdata[2690:10000]
STOxmld = STOdata["LH"]+2*STOdata["LV"] #+0.3
STOdata["Energy(eV)"] = STOdata["Energy(eV)"] - 780.4
STO_experiment = STOdata["LH"] - STOdata["LV"] - 0.8

N = 20	# 共有图片N张
M = 20	# 每M张合成一张纵向长图
G = int(N / M) 	# 共分为G组,也就是橫向

#####儲存的檔名,不含副檔名
name = '730_STO_XMCD'

def process(i):

    i_name = str(round((-1)*(i-1)*0.0005,4))
    #j_name = str(round((j-1)*0.0005,4))

    LS = pd.read_csv('C:/Users/Tim/Desktop/理論數據/Theory/LS/Co_210324_005_LS_728_XMCD__Hex0.0' +'_XAS.dat', sep="\s+",    encoding='utf-8',skiprows=6,engine='python',header=None ) 
    
    if i != 1:
         
        HS = pd.read_csv('C:/Users/Tim/Desktop/理論數據/Theory/HS/Co_210325_004_HS_729_XMCD_Hex' + i_name + '0' + '_XAS.dat', sep="\s+",    encoding='utf-8',skiprows=6,engine='python',header=None ) 
        #LS = pd.read_csv('C:/Users/Tim/Desktop/理論數據/Theory/LS/Co_210324_005_LS_728_XMCD__Hex' + i_name + '0' +'_XAS.dat', sep="\s+",    encoding='utf-8',skiprows=6,engine='python',header=None ) 
    
      
    if i == 1:
        
        HS = pd.read_csv('C:/Users/Tim/Desktop/理論數據/Theory/HS/Co_210325_004_HS_729_XMCD_Hex' + i_name  + '_XAS.dat', sep="\s+",    encoding='utf-8',skiprows=6,engine='python',header=None ) 
        #LS = pd.read_csv('C:/Users/Tim/Desktop/理論數據/Theory/LS/Co_210324_005_LS_728_XMCD__Hex' + i_name +'_XAS.dat', sep="\s+",    encoding='utf-8',skiprows=6,engine='python',header=None ) 
    
      
    # if i != 1:
    #     HS = pd.read_csv('C:/Users/Tim/Desktop/理論數據/Theory/HS/Co_210325_004_HS_728_XMCD_Hex' + j_name  + '_XAS.dat', sep="\s+",    encoding='utf-8',skiprows=6,engine='python',header=None ) 
    #     #LS = pd.read_csv('C:/Users/Tim/Desktop/理論數據/Theory/LS/Co_210324_005_LS_728_XMCD__Hex' + i_name + '0' +'_XAS.dat', sep="\s+",    encoding='utf-8',skiprows=6,engine='python',header=None ) 
    
      
    # if i == 1:
    #     HS = pd.read_csv('C:/Users/Tim/Desktop/理論數據/Theory/HS/Co_210325_004_HS_728_XMCD_Hex' + j_name + '_XAS.dat', sep="\s+",    encoding='utf-8',skiprows=6,engine='python',header=None ) 
    #     #LS = pd.read_csv('C:/Users/Tim/Desktop/理論數據/Theory/LS/Co_210324_005_LS_728_XMCD__Hex' + i_name +'_XAS.dat', sep="\s+",    encoding='utf-8',skiprows=6,engine='python',header=None ) 
    
      
    
    #####LS
    LS = LS[20:2000]

    chLSx = 0.16
    #####  LS polar x

    LSx_x = (LS[0]+chLSx).values

    LSx_y = LS[2].values

    LSx_y = -1*LSx_y-0.0054

    #####  LS polar y

    LSy_x = LSx_x
    LSy_y = (LS[4]).values

    LSy_y = -1*LSy_y-0.0054


    #####HS
    HS = HS[20:2000]

    chHSx = -0.23
    #####  HS polar x

    HSx_x = (HS[0]+chHSx).values

    HSx_y = HS[2].values

    HSx_y = -1*HSx_y-0.0044

    #####  HS polar y

    HSy_x = HSx_x

    HSy_y = HS[4].values

    HSy_y = -1*HSy_y-0.0044


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
    LSx_y = LSx_y + arct

    arct = f(HSx_x)
    HSy_y = HSy_y + arct
    HSx_y = HSx_y + arct



    #plt.plot(LSx_x,LSy_y,color='orange')
    #LV
    f = interp1d(HSx_x,HSy_y,fill_value='extrapolate')
    HSy_y = f(LSx_x)
    #plt.plot(LSx_x,HSy_y,color='orange')
    STOy = 1.8*(0.76*LSy_y + 0.24*HSy_y)-0.4 #-1.05+(i-1)*0.35
    #plt.plot(LSx_x,STOy,color='b')
    #LH
    f = interp1d(HSx_x,HSx_y,fill_value='extrapolate')
    HSx_y = f(LSx_x)
    STOz = 1.8*(0.76*LSx_y + 0.24*HSx_y)-0.4 #-1.05+(i-1)*0.35



    STO_theory = STOz - STOy - 0.8

    plt.plot(STOdata["Energy(eV)"],STOdata["LV"],label='experiment LV',color='b')
    plt.plot(STOdata["Energy(eV)"],STOdata["LH"],label='experiment LH',color='r')
    plt.plot(LSx_x,STOy,label= 'theory LV of LS Hex'+ '0.0' + ' HS' + i_name,color='b')
    plt.plot(LSx_x,STOz,label= 'theory LH of LS Hex'+ '0.0' + ' HS' + i_name,color='r')
    plt.plot(STOdata["Energy(eV)"],STO_experiment,label='experiment of LH-LV',color='black')
    plt.plot(LSx_x,STO_theory,label = 'theory of LH-LV',color='orange')
    # plt.plot(HSx_x,arct,color='g')
    
    plt.rc('legend',fontsize=5.5)
    plt.legend()    
    plt.grid(True)
    
    plt.xlim(-10,20)
    plt.title( 'STO XMCD 76%LS+24%HS  HSHex' +i_name )
    plt.savefig(name + '/' + '730_XMCD_HSHex' + i_name + '.png')
    plt.show(block=False)
    plt.pause(0.1)
    plt.close()

for i in range(1,M+1):
    process(i)


# M = N       # 如果仅需要合成单张图片，请解除此句的注释，令 M=N
# 路径可以是绝对路径，也可以是相对路径，注意路径中不能出现中文，否则无法被imread读取
img_path =  name + '/'



print(' image  :', N, '\n',
	   'length :', M, '\n',
	   'group  :', G)
himgs = []
for j in range(1, G+1):
    vimgs = []
   
	# 把一组图像存到imgs里面
    for i in range(1,M+1):
	    # 每个文件的路径
        i_name = str(round((-1)*(i-1)*0.0005,4))
        #j_name = str(round((j-1)*0.0005,4))
        path = img_path + '730_XMCD_HSHex' + i_name + '.png'
        tmp = cv2.imread(path)
        vimgs.append(tmp)
    
    tmp2 = np.vstack(vimgs)
    himgs.append(tmp2)
    
img = np.hstack(himgs)

cv2.imwrite('SumImageof'+ name + '.jpg', img)

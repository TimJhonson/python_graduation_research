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

toImage = Image.new('RGB', (600 * 3, 450 * 2))  # 构造图片的宽和高，如果图片不能填充完全会
dir_root = "C:/Users/Tim/Desktop/XMLD_XMCD/SUM"
files = os.listdir(dir_root)
count = 0
begin_x = 0
begin_y = 0
for file_name in files:
    fname = os.path.join(dir_root, file_name)
    fromImage = Image.open(fname)
    # fromImage = fromImage.resize((850, 1100))
    toImage.paste(fromImage, (begin_x, begin_y))
    begin_y += 450
    if begin_y % 900 == 0:
        begin_x += 600
        begin_y = 0

toImage.save('SumImageof'+ 'SUM.jpg')
import numpy as np
import cv2 as cv
from PIL import Image
import os
import timeit
start = timeit.default_timer() 
from tifffile import imsave
def mask_t(l,flag,t):
    d=l.shape
    k= np.zeros(d,dtype=np.uint8)
    if flag == 0:  
        temp=np.where(l<=t)
        k[temp]=255                                                
    elif flag == 1:        
        temp=np.where(l>=t)
        k[temp]=255
    return k

f1="c____img_white.tiff"#input_one
f2="c____output1.tif"#gans_output
l=[]
img1 = Image.open(f1)
l1 = np.array(img1)
img2 = Image.open(f2)
l2 = np.array(img2)
mask=mask_t(l1,0,300)

k = np.where(mask==255)
l=l1
print(l,"\n",l1)
l[k]=(l2[k])
imsave('final_output.tif',l)
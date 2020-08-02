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

def correrct(l,mask,mode=0):
    if mode==0:
        dst=cv.inpaint(l,mask,3,cv.INPAINT_NS)                   
    if mode==1:
        dst=cv.inpaint(l,mask,3,cv.INPAINT_TELEA)
    return dst 

    f1="c____img_white_24"#input_one
    f2="c____img_white_24._output1"#gans_output

    img1 = Image.open(f1)
    l1 = np.array(img1)
    img2 = Image.open(f2)
    l2 = np.array(img2)
    mask=mask_t(l,0,300)
    inpaint_arr = correrct(l,mask)
    k = np.where(mask==255)
    l=l1
    l[k]=(inpaint_arr[k]+l2[k])//2
    imsave('final_output.tif',l)


stop = timeit.default_timer()
print('Time: ', stop - start)
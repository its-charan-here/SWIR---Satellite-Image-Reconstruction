import numpy as np
import cv2 as cv
from PIL import Image
import os
import timeit
start = timeit.default_timer() 
from tifffile import imsave
from skimage.measure import compare_ssim
import argparse
import imutils
import cv2
import tifffile as tiff

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

img1=r""
img2=r""
img3=r""

original_img = tiff.imread(img1)
check_img = tiff.imread(img2)

input_img = tiff.imread(img3)

(score, diff) = compare_ssim(imageA, imageB, full=True)
diff = (diff * 255).astype("uint8")

print("SSIM: {}".format(score))

stop = timeit.default_timer()
print('Time: ', stop - start)
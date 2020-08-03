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

img1=r"D:\SIH 2020\NM391_The-Ones-n-Zeros\final_output\Day3_mentoring_Output\output_reshaped.tif"
img2=r"D:\SIH 2020\NM391_The-Ones-n-Zeros\final_output\Day3_mentoring_Output\horiz_data_op_359.tif"
img3=r"D:\SIH 2020\NM391_The-Ones-n-Zeros\final_output\Day3_mentoring_Output\hori_input_reshaped.tif"

original_img = tiff.imread(img1)
check_img = tiff.imread(img2)

input_img = tiff.imread(img3)

k = np.where(mask_t(input_img,0,300) != 225)
print("orig : ",original_img[k])
print("input : ",input_img[k])

(score, diff) = compare_ssim(original_img[k], input_img[k], full=True)
diff = (diff * 255).astype("uint8")

print("SSIM original and input img: {}".format(score))
# print("Diff in SSIM original and input img: {}".format(diff))

(score, diff) = compare_ssim(original_img[k], check_img[k], full=True)
diff = (diff * 255).astype("uint8")

print("SSIM original and check img: {}".format(score))
# print("Diff in SSIM original and check img: {}".format(diff))


stop = timeit.default_timer()
print('Time: ', stop - start)
import numpy as np
import cv2 as cv
from PIL import Image
import os
import timeit
start = timeit.default_timer() 
from tifffile import imsave
f=r"D:\SIH 2020\NM391_The-Ones-n-Zeros\final_output\Day3_mentoring_Output\horiz_data.tif"
img = Image.open(f)
l = np.array(img)
k=l[:8*(l.shape[0]//8),:8*(l.shape[1]//8)]
imsave("output_reshaped.tif",k)


stop = timeit.default_timer()
print('Time: ', stop - start)
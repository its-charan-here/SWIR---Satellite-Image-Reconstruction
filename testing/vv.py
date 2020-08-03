import numpy as np
import cv2 as cv
from PIL import Image
import os
import timeit
start = timeit.default_timer() 
from tifffile import imsave
f=""
img = Image.open(f)
l = np.array(img)
k=l[:8*(l.shape[0]//8),:8*(l.shape[1]//8)]
imsave("output_reshaped",l)


stop = timeit.default_timer()
print('Time: ', stop - start)
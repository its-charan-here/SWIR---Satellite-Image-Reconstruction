import numpy as np
import cv2 as cv
from PIL import Image
import timeit
start = timeit.default_timer() 


def mask_t(l,flag,t):
    d=l.shape
    k= np.zeros(d,dtype=np.uint8)
    if flag == 0:  
        temp=np.where(l>=t)
        k[temp]=255                                                
    elif flag == 1:        
        temp=np.where(l<=t)
        k[temp]=255
    return k


       
f="vert_data.tif"
img = Image.open(f)

l = np.array(img)
t=Image.fromarray(mask_t(l,0,300))
t.save("vert_mask.png")
stop = timeit.default_timer()
print('Time: ', stop - start)
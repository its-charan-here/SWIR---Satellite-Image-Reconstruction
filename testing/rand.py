import random
import numpy as np
from PIL import Image
from tifffile import imsave
import tifffile as tif
import timeit
start = timeit.default_timer() 
import os

def array_to_jpg_image(f):
    l=(f*(255/4095))//1
    gray=np.uint8(l)
    im = Image.fromarray(gray)
    return im

def f_up(fol):
    t=random.randrange(2,4000)
    w=random.randrange(1,7)
    fol[:,t:t+w]=0
    return l
dt =np.dtype(np.uint16)
f=os.listdir('dat')
for _ in f:
    img= tif.imread("dat/"+_)
    l = np.array(img,dtype=dt)
    #print(l.dtype,img.dtype)

    l=f_up(l)
    n=5
    while random.randrange(1,20)>=2:
        l=f_up(l)
    imsave("veri/c____"+_,l)
    array_to_jpg_image(l).save("veri_jpg/c____"+_[:-4]+".jpg")
stop = timeit.default_timer()
print('Time: ', stop - start)
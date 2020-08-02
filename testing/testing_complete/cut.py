import numpy as np
from PIL import Image
import timeit
from tifffile import imsave
start = timeit.default_timer() 

dt =np.dtype(np.int16)
l= np.fromfile('black.rl0', dtype=dt).reshape((8238,6000))
for i in range(20):
    for j in range(25):
        x=320*j
        y=300*i
        k=l[x:x+320,y:y+300]
        s=str(i)+"_"+str(j)
        s=s+'.tif'
        imsave(s,k)
stop = timeit.default_timer()
print('Time: ', stop - start)

import numpy as np
from PIL import Image
import timeit
start = timeit.default_timer() 

dt =np.dtype(np.int16)
l= np.fromfile('black.rl0', dtype=dt).reshape((8238,6000))
for i in range(18):
    for j in range(25):
        x=320*j
        y=320*i
        k=l[x:x+320,y:y+320]
        s=str(i)+" "+str(j)
        s="../"+s+'.tif'
        Image.fromarray(k).save(s)
stop = timeit.default_timer()
print('Time: ', stop - start)

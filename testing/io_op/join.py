import numpy as np
from PIL import Image
import timeit
from tifffile import imsave
start = timeit.default_timer() 


f=sys.argv[1]

for _ in os.listdir(f):

    img = Image.open(f+_)
    l = np.array(img)
    for i in range(l.shape[1]//320):
        for j in range(l.shape[0]//320):
            x=320*j
            y=320*i
            k=l[x:x+320,y:y+320]
            s=_+str(i)+"_"+str(j)
            s=f+"/temp/"+s+'.tif'
            imsave(s,k)
stop = timeit.default_timer()
print('Time: ', stop - start)

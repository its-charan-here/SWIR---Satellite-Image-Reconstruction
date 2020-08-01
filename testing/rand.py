import random
import numpy as np
from PIL import Image
import timeit
start = timeit.default_timer() 
import os

def f_up(fol):
    t=random.randrange(2,270);
    w=random.randrange(1,6);
    fol[t:t+w,:]=0
    return l

f=os.listdir('data black')
for _ in f:
    img = Image.open("data black/"+_)
    l = np.array(img)
    l=f_up(l)
    l=f_up(l)
    while random.randrange(1,9)>=7:
        l=f_up(l)
    Image.fromarray(l).save("c__H___"+_)
stop = timeit.default_timer()
print('Time: ', stop - start)
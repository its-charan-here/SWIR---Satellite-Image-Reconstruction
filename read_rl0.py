import os
import sys
import PIL
from PIL import Image
import numpy as np
import timeit

def mask_t(f,flag,t,output):    

    l=f
    dt1 =np.dtype(np.uint8)
    k= np.zeros(l.shape,dtype=dt1)
   
    if flag == 0:  
        temp=np.where(l<=t)
        k[temp]=255                                                       
                        
    elif flag == 1:        
        temp=np.where(l>=t)
        k[temp]=255
                       

    print(l,"\n",k)
    print(flag,t)
    np.save(output,k)
    return k
     
    
def con_rl(name,byte): # converter function , 
    f= np.load(name)
    final=f
    name=name[:-4]+"_new.rl0"
    fi=open(name,"wb")
    for i in range(d[0]):
        for j in range(d[1]):
            fi.write(int(f[i][j]).to_bytes(byte, 'big'))
    fi.close()
    




if __name__ == "__main__":
    
    start = timeit.default_timer()
    
    f="horiz_data.tif"
    t=350
    img = Image.open(f)
    flag=0 
    img_arr = np.array(img)
    output='mask_horiz.npy'
    
    t=Image.fromarray(mask_t(img_arr,flag,t,output))
    t.save("mask_h.tif")
    np.save('horiz_input.npy',img_arr)
    
    stop = timeit.default_timer()
    print('Time: ', stop - start)












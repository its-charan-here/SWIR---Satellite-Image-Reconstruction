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
        temp=np.where(l>=t)
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
    

def correction(f,mask,d,output='corrected_img.npy'): # error correct7ion , mask value as input and original file as input , generalised avereage function. 
    dt =np.dtype(np.uint16)
    l= np.fromfile(f, dtype=dt).reshape((8238,6000))
    k= np.load(mask)
    
    def pas(i,j):
        avg,t=0,0
        for x,y in [[1,1],[-1,-1],[0,1],[0,-1],[-1,1],[1,-1]]:
            try:
                avg+=l[i+x,j+y]
                t+=1
            except:
                avg+=0
        l[i,j]=avg/t

    print(k)
    for i in range(d[0]):
        for j in range(d[1]):
                
                if k[i][j] != 0:
                    print(l[i,j],k[i][j])
                    pas(i,j)
                    print(l[i,j])

    np.save(output,l)
    return output 


if __name__ == "__main__":
    
    start = timeit.default_timer()
<<<<<<< HEAD
    
    f="vert_data.tif"
=======
    d=(8238,6000)
    f="hori_data.tif"
>>>>>>> ff8e77d5c2e74df02b5e03f7612a08a1148e2e01
    t=350
    img = Image.open(f)
    flag=0 
    img_arr = np.array(img)
    output='mask_verti.npy'
    
    t=Image.fromarray(mask_t(img_arr,flag,t,output))
    t.save("mask.tif")
    np.save('verti_input.npy',img_arr)
    
    stop = timeit.default_timer()
    print('Time: ', stop - start)












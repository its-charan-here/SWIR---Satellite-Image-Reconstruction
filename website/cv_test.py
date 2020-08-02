import numpy as np
import cv2 as cv
from PIL import Image
import timeit
start = timeit.default_timer() 

# def con_rl(f,name,byte):
#     name=name+".rl0"
#     fi=open(name,"wb")

#     for i in range(d[0]):
#        for j in range(d[1]):
#            fi.write(int(f[i][j]).to_bytes(byte, 'little'))
#     fi.close()
#     #f.astype('<H').tofile(name)

def array_to_jpg_image(f):
    l=(f*(255/4095))//1
    gray=np.uint8(l)
    im = Image.fromarray(gray)
    return im

def mask_t(l,flag,t):
    d=l.shape
    k= np.zeros(d,dtype=np.uint8)
    if flag == 0:  
        temp=np.where(l<=t)
        k[temp]=255                                                
    elif flag == 1:        
        temp=np.where(l>=t)
        k[temp]=255
    return k

def correrct(l,mask,mode=0):
    if mode==0:
        dst=cv.inpaint(l,mask,3,cv.INPAINT_NS)                   
    if mode==1:
        dst=cv.inpaint(l,mask,3,cv.INPAINT_TELEA)
    return dst    


f=r"uploads/image.tif"



img = Image.open(f)
l = np.array(img)
inpaint_arr = correrct(l,mask_t(l,0,300),1)
t=Image.fromarray(inpaint_arr)


t.save("views/cvoutput.tif")

array_to_jpg_image(inpaint_arr).save("views/cvoutput.jpg")


stop = timeit.default_timer()
print('Time: ', stop - start)